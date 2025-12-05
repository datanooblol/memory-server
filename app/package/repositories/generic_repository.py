from typing import TypeVar, Generic, List, Optional, Dict, Any, Type
from pydantic import BaseModel
from datetime import datetime
import json

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
    
    async def get_by_id(self, id: str) -> Optional[T]:
        results = await self.storage.query(
            f'SELECT * FROM {self.table_name} WHERE "{self.id_field}" = ?',
            {self.id_field: id}
        )
        if results:
            deserialized_data = self._deserialize_from_storage(results[0])
            return self.model_class(**deserialized_data)
        return None
    
    async def find_by(self, filters: Dict[str, Any]) -> List[T]:
        where_parts = []
        params = {}
        
        for key, value in filters.items():
            where_parts.append(f'"{key}" = ?')
            params[key] = value
        
        where_clause = " AND ".join(where_parts) if where_parts else "1=1"
        
        results = await self.storage.query(
            f"SELECT * FROM {self.table_name} WHERE {where_clause}",
            params
        )
        
        return [self.model_class(**self._deserialize_from_storage(row)) for row in results]
    
    async def update(self, id: str, model: T) -> None:
        data = model.dict()
        serialized_data = self._serialize_for_storage(data)
        
        # Remove the ID from data to avoid updating it
        serialized_data.pop(self.id_field, None)
        
        await self.storage.update(self.table_name, serialized_data, {self.id_field: id})
    
    async def delete(self, id: str) -> None:
        await self.storage.query(
            f'DELETE FROM {self.table_name} WHERE "{self.id_field}" = ?',
            {self.id_field: id}
        )