# storage/interfaces.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class RelationalStorage(ABC):
    @abstractmethod
    async def create_table(self, table_name: str, schema: Dict) -> None:
        pass
    
    @abstractmethod
    async def insert(self, table: str, data: Dict) -> Any:
        pass
    
    @abstractmethod
    async def query(self, sql: str, params: Dict = None) -> List[Dict]:
        pass
    
    @abstractmethod
    async def update(self, table: str, data: Dict, where: Dict) -> None:
        pass

class VectorStorage(ABC):
    @abstractmethod
    async def create_collection(self, collection: str) -> None:
        pass
    
    @abstractmethod
    async def insert_embedding(self, collection: str, id: str, vector: List[float], metadata: Dict) -> None:
        pass
    
    @abstractmethod
    async def search_similar(self, collection: str, vector: List[float], limit: int = 10) -> List[Dict]:
        pass

class NoSQLStorage(ABC):
    @abstractmethod
    async def create_table(self, table_name: str, key_schema: Dict) -> None:
        pass
    
    @abstractmethod
    async def put_item(self, table: str, item: Dict) -> None:
        pass
    
    @abstractmethod
    async def get_item(self, table: str, key: Dict) -> Optional[Dict]:
        pass
    
    @abstractmethod
    async def scan_items(self, table: str, filters: Dict = None) -> List[Dict]:
        pass
