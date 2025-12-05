from typing import TypeVar, Generic, List, Optional, Dict, Any, Type
from pydantic import BaseModel
from datetime import datetime

T = TypeVar('T', bound=BaseModel)

class NoSQLRepository(Generic[T]):
    def __init__(self, storage, model_class: Type[T], table_name: str, partition_key: str):
        self.storage = storage
        self.model_class = model_class
        self.table_name = table_name
        self.partition_key = partition_key
    
    async def create(self, model: T) -> str:
        item = model.dict()
        # Convert datetime to ISO string for DynamoDB
        for key, value in item.items():
            if isinstance(value, datetime):
                item[key] = value.isoformat()
            elif isinstance(value, list) and value is not None:
                item[key] = value  # DynamoDB handles lists natively
            elif isinstance(value, dict) and value is not None:
                item[key] = value  # DynamoDB handles dicts natively
        
        await self.storage.put_item(self.table_name, item)
        return getattr(model, self.partition_key)
    
    async def get_by_id(self, id: str) -> Optional[T]:
        item = await self.storage.get_item(
            self.table_name, 
            {self.partition_key: id}
        )
        return self.model_class(**item) if item else None
    
    async def find_by(self, filters: Dict[str, Any]) -> List[T]:
        items = await self.storage.scan_items(self.table_name, filters)
        return [self.model_class(**item) for item in items]
    
    async def update(self, id: str, model: T) -> None:
        # For DynamoDB, update is same as put (upsert)
        await self.create(model)
    
    async def delete(self, id: str) -> None:
        table_obj = self.storage.dynamodb.Table(self.table_name)
        table_obj.delete_item(Key={self.partition_key: id})