import aiosqlite
from typing import Dict, List, Any
from ..base import RelationalStorage

class SQLiteStorage(RelationalStorage):
    def __init__(self, config: Dict):
        self.db_path = config["path"]
    
    async def create_table(self, table_name: str, schema: Dict) -> None:
        # Escape column names with quotes to handle reserved keywords
        columns = ", ".join([f'"{col}" {dtype}' for col, dtype in schema.items()])
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(sql)
            await db.commit()
    
    async def insert(self, table: str, data: Dict) -> Any:
        columns = ", ".join([f'"{col}"' for col in data.keys()])
        placeholders = ", ".join(["?" for _ in data])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(sql, list(data.values()))
            await db.commit()
            return cursor.lastrowid
    
    async def query(self, sql: str, params: Dict = None) -> List[Dict]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(sql, list(params.values()) if params else [])
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def update(self, table: str, data: Dict, where: Dict) -> None:
        set_clause = ", ".join([f'"{col}" = ?' for col in data.keys()])
        where_clause = " AND ".join([f'"{col}" = ?' for col in where.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(sql, list(data.values()) + list(where.values()))
            await db.commit()