# Storage Factory Design

## Overview
Plug-and-play storage architecture allowing mix-and-match of different storage backends through configuration without code changes.

## Current Implementation

### Interface Layer (IMPLEMENTED)
- `RelationalStorage` - Abstract interface for SQL-like operations (CREATE, INSERT, UPDATE, DELETE, SELECT)
- `VectorStorage` - Abstract interface for embedding operations (CREATE_COLLECTION, INSERT_EMBEDDING, SEARCH_SIMILAR)
- `NoSQLStorage` - Abstract interface for NoSQL operations (PUT_ITEM, GET_ITEM, SCAN_ITEMS)

### Implementation Layer (IMPLEMENTED)
- `SQLiteStorage` - SQLite with aiosqlite, context managers, escaped column names
- `DuckDBStorage` - DuckDB with context managers, escaped column names
- `DynamoDBStorage` - AWS DynamoDB with boto3, partition key support
- `VectorDuckDBStorage` - DuckDB vector extension (placeholder)

### Factory Layer (IMPLEMENTED)
- `StorageFactory` - Creates storage instances based on type
  - `create_relational()` - SQLite, DuckDB
  - `create_nosql()` - DynamoDB
  - `create_vector()` - (planned)
- `StorageManager` - YAML-driven configuration management

## Current Configuration

```yaml
relational:
  user_data_sqlite:
    type: "sqlite"
    config: {path: "data/users.db"}
  user_data_duckdb:
    type: "duckdb"
    config: {path: "data/users.duckdb"}

nosql:
  user_data_dynamodb:
    type: "dynamodb"
    config:
      region: "us-east-1"
      access_key: "<access_key>"
      secret_key: "<secret_key>"
```

## Usage Pattern (IMPLEMENTED)

```python
storage_manager = StorageManager("app/config/storage.yaml")

# Different backends for same data
sqlite_storage = storage_manager.get_relational("user_data_sqlite")
duckdb_storage = storage_manager.get_relational("user_data_duckdb")
dynamodb_storage = storage_manager.get_nosql("user_data_dynamodb")

# Same repository interface works with all
repo_factory = RepositoryFactory(sqlite_storage)  # or any storage
user_repo = repo_factory.get_user_repository()
```

## Key Features (IMPLEMENTED)

### SQL Reserved Keyword Handling
- All column names escaped with double quotes
- Handles `references`, `order`, `group` etc. safely
- Works across SQLite and DuckDB

### JSON Serialization
- Complex types (List, Dict) automatically serialized to JSON strings
- Boolean values converted to 0/1 for SQL databases
- Automatic deserialization when reading data

### Context Manager Usage
- SQLite: `async with aiosqlite.connect()` for proper cleanup
- DuckDB: `with duckdb.connect()` for automatic WAL cleanup
- No persistent connections to avoid resource leaks

### Auto-Detection Repository
- Repository factory detects storage type automatically
- Returns `GenericRepository` for SQL storage
- Returns `NoSQLRepository` for NoSQL storage
- Same interface, different implementations

## File Structure (CURRENT)

```
app/package/storage/
├── base.py                    # Abstract interfaces
├── factory.py                 # Storage factory
├── manager.py                 # Configuration manager
├── relational/
│   ├── sqlite.py             # SQLite implementation
│   └── duckdb.py             # DuckDB implementation
├── nosql/
│   └── dynamodb.py           # DynamoDB implementation
└── vector/
    └── duckdb.py             # Vector storage (placeholder)

app/package/repositories/
├── factory.py                 # Repository factory
├── generic_repository.py      # SQL repository
└── nosql_repository.py        # NoSQL repository

app/package/schemas/
└── __init__.py               # SQL table schemas

app/config/
└── storage.yaml              # Storage configuration
```

## Benefits (PROVEN)

- **Multi-Backend Support**: Same code works with SQLite, DuckDB, DynamoDB
- **Configuration-Driven**: Switch backends via YAML config only
- **Type Safety**: Pydantic models ensure data validation
- **Complex Data Support**: JSON serialization for lists, dicts, nested objects
- **Reserved Keyword Safe**: Proper SQL escaping prevents syntax errors
- **Resource Management**: Context managers prevent connection leaks
- **Testing Friendly**: Easy to mock repositories and test with different backends

## Adding New Storage Backend

1. Implement appropriate interface (`RelationalStorage`, `NoSQLStorage`, or `VectorStorage`)
2. Add to factory's create method
3. Update config YAML
4. Repository factory automatically detects and uses new backend
5. All existing models work immediately

## Tested Scenarios

- ✅ User CRUD operations on SQLite and DuckDB
- ✅ Complex data types (references list, source_path dict)
- ✅ Reserved keyword handling (references column)
- ✅ Multi-model relationships (User → Project → ChatSession → Conversation)
- ✅ JSON serialization/deserialization
- ✅ Bangkok timezone handling
- ✅ DynamoDB NoSQL operations
- ✅ Automatic repository type detection