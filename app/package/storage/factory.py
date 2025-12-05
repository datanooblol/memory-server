from typing import Dict
from .base import RelationalStorage, NoSQLStorage
from .relational.sqlite import SQLiteStorage
from .relational.duckdb import DuckDBStorage
from .nosql.dynamodb import DynamoDBStorage

class StorageFactory:
    @staticmethod
    def create_relational(storage_type: str, config: Dict) -> RelationalStorage:
        if storage_type == "sqlite":
            return SQLiteStorage(config)
        elif storage_type == "duckdb":
            return DuckDBStorage(config)
        else:
            raise ValueError(f"Unknown relational storage: {storage_type}")
    
    @staticmethod
    def create_nosql(storage_type: str, config: Dict) -> NoSQLStorage:
        if storage_type == "dynamodb":
            return DynamoDBStorage(config)
        else:
            raise ValueError(f"Unknown NoSQL storage: {storage_type}")