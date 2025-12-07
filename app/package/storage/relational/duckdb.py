import duckdb
import json
from typing import Dict, List, Any
from ..base import RelationalStorage

class DuckDBStorage(RelationalStorage):
    def __init__(self, config: Dict):
        self.db_path = config["path"]
    
    async def create_table(self, table_name: str, schema: Dict) -> None:
        # Escape column names with quotes to handle reserved keywords
        columns = ", ".join([f'"{col}" {dtype}' for col, dtype in schema.items()])
        sql = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns})'
        
        with duckdb.connect(self.db_path) as conn:
            conn.execute(sql)
    
    async def insert(self, table: str, data: Dict) -> Any:
        columns = ", ".join([f'"{col}"' for col in data.keys()])
        placeholders = ", ".join(["?" for _ in data])
        sql = f'INSERT INTO "{table}" ({columns}) VALUES ({placeholders})'
        
        # Serialize complex types to JSON
        values = [json.dumps(v) if isinstance(v, (dict, list)) else v for v in data.values()]
        
        with duckdb.connect(self.db_path) as conn:
            cursor = conn.execute(sql, values)
            return cursor.fetchone()
    
    async def query(self, sql: str, params: Dict = None) -> List[Dict]:
        with duckdb.connect(self.db_path) as conn:
            if params:
                cursor = conn.execute(sql, list(params.values()))
            else:
                cursor = conn.execute(sql)
            
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            result = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                # Try to deserialize JSON strings back to objects
                for key, value in row_dict.items():
                    if isinstance(value, str):
                        try:
                            row_dict[key] = json.loads(value)
                        except (json.JSONDecodeError, TypeError):
                            pass  # Keep as string if not valid JSON
                result.append(row_dict)
            return result
    
    async def update(self, table: str, data: Dict, where: Dict) -> None:
        set_clause = ", ".join([f'"{col}" = ?' for col in data.keys()])
        where_clause = " AND ".join([f'"{col}" = ?' for col in where.keys()])
        sql = f'UPDATE "{table}" SET {set_clause} WHERE {where_clause}'
        
        with duckdb.connect(self.db_path) as conn:
            conn.execute(sql, list(data.values()) + list(where.values()))
