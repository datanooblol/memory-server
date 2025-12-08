from typing import TypeVar, Generic, List, Optional, Dict, Any, Type
from pydantic import BaseModel
from datetime import datetime
import json
from package.data_models.base import bangkok_now

T = TypeVar('T', bound=BaseModel)

class GenericRepository(Generic[T]):
    def __init__(self, storage, model_class: Type[T], table_name: str, id_field: str):
        self.storage = storage
        self.model_class = model_class
        self.table_name = table_name
        self.id_field = id_field
    
    def _serialize_for_storage(self, data: Dict) -> Dict:
        """Convert complex types to storage-friendly format"""
        serialized = {}
        for key, value in data.items():
            if isinstance(value, datetime):
                serialized[key] = value.isoformat()
            elif isinstance(value, list):
                serialized[key] = json.dumps(value) if value is not None else None
            elif isinstance(value, dict):
                serialized[key] = json.dumps(value) if value is not None else None
            elif isinstance(value, bool):
                serialized[key] = 1 if value else 0  # For SQLite/DuckDB
            else:
                serialized[key] = value
        return serialized
    
    def _deserialize_from_storage(self, data: Dict) -> Dict:
        """Convert storage format back to Python types"""
        deserialized = {}
        for key, value in data.items():
            if value is None:
                deserialized[key] = None
            elif key in ['references', 'convo_ids', 'parent_episode_ids', 'tasks', 'sample_values']:
                # These are JSON fields
                try:
                    deserialized[key] = json.loads(value) if value else None
                except (json.JSONDecodeError, TypeError):
                    deserialized[key] = value
            elif key == 'source_path':
                # Dict field
                try:
                    deserialized[key] = json.loads(value) if value else {}
                except (json.JSONDecodeError, TypeError):
                    deserialized[key] = value
            elif key == 'active':
                # Boolean field
                deserialized[key] = bool(value) if isinstance(value, int) else value
            else:
                deserialized[key] = value
        return deserialized
    
    async def create(self, model: T) -> str:
        data = model.dict()
        serialized_data = self._serialize_for_storage(data)
        
        await self.storage.insert(self.table_name, serialized_data)
        return getattr(model, self.id_field)
    
    async def batch_create(self, models: List[T]) -> List[str]:
        ids = []
        for model in models:
            await self.create(model)
            ids.append(getattr(model, self.id_field))
        return ids

    async def get_by_id(self, id: str) -> Optional[T]:
        results = await self.storage.query(
            f'SELECT * FROM "{self.table_name}" WHERE "{self.id_field}" = ?',
            {self.id_field: id}
        )
        if results:
            deserialized_data = self._deserialize_from_storage(results[0])
            return self.model_class(**deserialized_data)
        return None
    
    async def find_by(self, filters: Dict[str, Any], order_by: str = "created_at") -> List[T]:
        where_parts = []
        params = {}
        
        for key, value in filters.items():
            where_parts.append(f'"{key}" = ?')
            params[key] = value
        
        where_clause = " AND ".join(where_parts) if where_parts else "1=1"
        
        results = await self.storage.query(
            f'SELECT * FROM "{self.table_name}" WHERE {where_clause} ORDER BY "{order_by}" ASC',
            params
        )
        
        return [self.model_class(**self._deserialize_from_storage(row)) for row in results]
    
    async def update(self, id: str, model: T) -> None:
        data = model.model_dump()
        serialized_data = self._serialize_for_storage(data)
        
        # Remove fields that shouldn't be updated
        serialized_data.pop(self.id_field, None)
        serialized_data.pop('created_at', None)
        
        await self.storage.update(self.table_name, serialized_data, {self.id_field: id})

    async def batch_update(self, updates: List[T]) -> int:
        """Update multiple records in single query"""
        count = 0
        
        if not updates:
            return count

        for model in updates:
            try:
                model.updated_at = bangkok_now()
                id_field = getattr(model, self.id_field)
                await self.update(id_field, model)
                count += 1
            except Exception:
                continue
        return count
        

    async def patch(self, id: str, partial_data: Dict[str, Any]) -> None:
        # Get existing record
        existing = await self.get_by_id(id)
        if not existing:
            raise ValueError("Record not found")
        
        # Merge partial data with existing
        existing_dict = existing.model_dump()
        existing_dict.update(partial_data)

        data = self.model_class(**existing_dict).model_dump()
        serialized_data = self._serialize_for_storage(data)

        serialized_data.pop(self.id_field, None)
        serialized_data.pop('created_at', None)
        
        await self.storage.update(self.table_name, serialized_data, {self.id_field: id})

    
    async def delete(self, id: str) -> None:
        await self.storage.query(
            f'DELETE FROM "{self.table_name}" WHERE "{self.id_field}" = ?',
            {self.id_field: id}
        )

    async def delete_by(self, filters: Dict[str, Any]) -> int:
        """Delete records matching criteria and return count of deleted records"""
        where_parts = []
        params = {}
        
        for key, value in filters.items():
            where_parts.append(f'"{key}" = ?')
            params[key] = value
        
        where_clause = " AND ".join(where_parts) if where_parts else "1=1"
        
        # Get count first (optional)
        count_results = await self.storage.query(
            f'SELECT COUNT(*) as count FROM "{self.table_name}" WHERE {where_clause}',
            params
        )
        count = count_results[0]['count'] if count_results else 0
        
        # Delete records
        await self.storage.query(
            f'DELETE FROM "{self.table_name}" WHERE {where_clause}',
            params
        )
        return count

    async def get_last_n(self, n: int, order_by: str = "created_at") -> List[T]:
        """Get last n records ordered by timestamp (newest first)"""
        results = await self.storage.query(
            f'SELECT * FROM "{self.table_name}" ORDER BY "{order_by}" DESC LIMIT ?',
            {"limit": n}
        )
        return [self.model_class(**self._deserialize_from_storage(row)) for row in results]
    
    async def get_first_n(self, n: int, order_by: str = "created_at") -> List[T]:
        """Get first n records ordered by timestamp (oldest first)"""
        results = await self.storage.query(
            f'SELECT * FROM "{self.table_name}" ORDER BY "{order_by}" ASC LIMIT ?',
            {"limit": n}
        )
        return [self.model_class(**self._deserialize_from_storage(row)) for row in results]