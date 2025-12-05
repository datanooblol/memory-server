# Data Access Architecture

## Overview
Multi-layered data access pattern enabling flexible backend integration while maintaining type safety and business logic separation.

## Current Implementation Status: ✅ FULLY IMPLEMENTED

## Architecture Layers

```
┌─────────────────────────┐
│   Application Code      │ ✅ Tests implemented
├─────────────────────────┤
│   Data Models           │ ✅ 10 Pydantic models with Bangkok timezone
│   (Type Safety)        │     BaseTimestampModel, JSON serialization
├─────────────────────────┤
│   Repository Pattern    │ ✅ Generic + NoSQL repositories
│   (Business Logic)     │     Auto-detection, CRUD operations
├─────────────────────────┤
│   Storage Interface     │ ✅ Relational, NoSQL, Vector interfaces
│   (Database Abstraction)│     Reserved keyword handling
├─────────────────────────┤
│   Storage Backends      │ ✅ SQLite, DuckDB, DynamoDB
│   (Implementation)     │     Context managers, JSON support
└─────────────────────────┘
```

## Components (IMPLEMENTED)

### 1. Data Models (Pydantic) ✅
- **Purpose**: Define data structure and validation
- **Location**: `app/package/data_models/*.py`
- **Implemented**: User, Project, ChatSession, Conversation, Source, AgentExecution, Episode, Metadata, FieldMetadata
- **Features**: Bangkok timezone, Field descriptions, Embedding text generation
- **Benefits**: Type safety, automatic validation, JSON serialization

### 2. Repository Pattern ✅
- **Purpose**: Business logic and data operations
- **Location**: `app/package/repositories/*.py`
- **Implemented**: GenericRepository (SQL), NoSQLRepository (NoSQL), RepositoryFactory
- **Features**: Auto-detection, JSON serialization, Complex type handling
- **Benefits**: Consistent API, testable, backend-agnostic

### 3. Storage Interface ✅
- **Purpose**: Abstract database operations
- **Location**: `app/package/storage/base.py`
- **Implemented**: RelationalStorage, NoSQLStorage, VectorStorage (placeholder)
- **Features**: Reserved keyword handling, Context manager support
- **Benefits**: Backend flexibility, easy testing

### 4. Storage Backends ✅
- **Purpose**: Actual database implementations
- **Location**: `app/package/storage/{relational,nosql,vector}/`
- **Implemented**: SQLiteStorage, DuckDBStorage, DynamoDBStorage
- **Features**: Escaped column names, JSON support, Context managers
- **Benefits**: Pluggable, configurable, optimized per use case

## Implementation Flow (WORKING)

### Generic Repository with JSON Support
```python
class GenericRepository(Generic[T]):
    def _serialize_for_storage(self, data: Dict) -> Dict:
        # Convert datetime → ISO string
        # Convert list/dict → JSON string
        # Convert bool → 0/1
    
    def _deserialize_from_storage(self, data: Dict) -> Dict:
        # Convert JSON strings back to Python objects
    
    async def create(self, model: T) -> str:
        serialized = self._serialize_for_storage(model.dict())
        await self.storage.insert(self.table_name, serialized)
```

### Auto-Detection Repository Factory
```python
class RepositoryFactory:
    def _get_repository(self, model_class, table_name, id_field):
        if hasattr(self.storage, 'put_item'):  # NoSQL
            return NoSQLRepository(self.storage, model_class, table_name, id_field)
        else:  # SQL
            return GenericRepository(self.storage, model_class, table_name, id_field)
```

### Multi-Backend Usage
```python
# Same code works with any backend
storage_manager = StorageManager("app/config/storage.yaml")

# SQLite backend
sqlite_storage = storage_manager.get_relational("user_data_sqlite")
sqlite_repo = RepositoryFactory(sqlite_storage).get_user_repository()

# DuckDB backend
duckdb_storage = storage_manager.get_relational("user_data_duckdb")
duckdb_repo = RepositoryFactory(duckdb_storage).get_user_repository()

# DynamoDB backend
dynamodb_storage = storage_manager.get_nosql("user_data_dynamodb")
dynamodb_repo = RepositoryFactory(dynamodb_storage).get_user_repository()

# Same operations work on all
user = User(email="test@example.com", password="secret")
await sqlite_repo.create(user)
await duckdb_repo.create(user)
await dynamodb_repo.create(user)
```

## Benefits

### Flexibility
- **Backend Switching**: Change database via configuration
- **Mixed Backends**: Different models can use different databases
- **Easy Testing**: Mock repositories for unit tests

### Maintainability
- **Separation of Concerns**: Each layer has single responsibility
- **Type Safety**: Pydantic ensures data integrity
- **Consistent API**: Same methods across all models

### Scalability
- **Performance Optimization**: Choose optimal backend per data type
- **Independent Scaling**: Scale different data stores independently
- **Future-Proof**: Easy to add new backends or models

## File Structure (CURRENT)

```
app/package/
├── data_models/                    # ✅ 10 Pydantic models
│   ├── base.py                    # BaseTimestampModel with Bangkok timezone
│   ├── user.py                    # User with email, password
│   ├── project.py                 # Project with user relationship
│   ├── chat_session.py            # ChatSession with project relationship
│   ├── conversation.py            # Conversation with references list
│   ├── source.py                  # Source with path dict
│   ├── agent_execution.py         # AgentExecution with tasks list
│   ├── episode.py                 # Episode with hierarchical rollups
│   ├── metadata.py                # Metadata with embedding text
│   └── reference.py               # Reference (deprecated)
├── repositories/                   # ✅ Repository pattern
│   ├── factory.py                 # Auto-detection factory
│   ├── generic_repository.py      # SQL repository with JSON support
│   └── nosql_repository.py        # NoSQL repository
├── schemas/                        # ✅ SQL table schemas
│   └── __init__.py               # Cross-compatible schemas
├── storage/                        # ✅ Storage backends
│   ├── base.py                    # Abstract interfaces
│   ├── factory.py                 # Multi-type factory
│   ├── manager.py                 # YAML configuration
│   ├── relational/
│   │   ├── sqlite.py             # SQLite with context managers
│   │   └── duckdb.py             # DuckDB with context managers
│   ├── nosql/
│   │   └── dynamodb.py           # DynamoDB implementation
│   └── vector/
│       └── duckdb.py             # Vector storage (placeholder)
└── __init__.py

app/config/                         # ✅ Configuration
└── storage.yaml                   # Multi-backend config

app/tests/                          # ✅ Comprehensive tests
├── test_all_models.py             # Multi-backend testing
├── test_user.py                   # User-specific tests
└── test_dynamodb.py               # DynamoDB tests
```

## Configuration (WORKING)

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

vector:  # Planned
  metadata:
    type: "chroma"
    config: {path: "./chroma_db"}
```

## Development Workflow (PROVEN)

### Adding New Model ✅
1. Create Pydantic model inheriting from `BaseTimestampModel`
2. Add schema to `schemas/__init__.py`
3. Add repository method to `RepositoryFactory`
4. Works immediately with SQLite, DuckDB, DynamoDB

### Adding New Backend ✅
1. Implement appropriate interface (`RelationalStorage`, `NoSQLStorage`)
2. Add to `StorageFactory.create_*()` method
3. Update `storage.yaml` configuration
4. Repository factory auto-detects and uses new backend
5. All 10 models work automatically

### Complex Data Types ✅
1. Use `List[str]`, `Dict[str, Any]` in Pydantic models
2. Generic repository automatically serializes to JSON
3. Deserialization happens transparently on read
4. Works across all SQL and NoSQL backends

### Reserved Keywords ✅
1. Use any column name (including `references`, `order`, `group`)
2. Storage implementations automatically escape with quotes
3. Works across SQLite and DuckDB without issues

## Testing Strategy (IMPLEMENTED)

### Multi-Backend Tests ✅
- **test_all_models.py**: Tests all 10 models on SQLite and DuckDB
- **test_user.py**: User-specific operations on multiple backends
- **test_dynamodb.py**: NoSQL operations with DynamoDB

### Proven Scenarios ✅
- **Complex relationships**: User → Project → ChatSession → Conversation
- **JSON serialization**: Lists (references), Dicts (source_path), Booleans (active)
- **Reserved keywords**: `references` column works without issues
- **Timezone handling**: Bangkok timezone in all timestamps
- **Backend switching**: Same code, different storage via config

### Performance Features ✅
- **Context managers**: Automatic connection cleanup
- **No persistent connections**: Prevents resource leaks
- **WAL file cleanup**: DuckDB properly closes connections
- **Batch operations**: JSON serialization optimized

## Migration Strategy (COMPLETED)

### Phase 1: Foundation ✅
- ✅ Generic repository with CRUD operations
- ✅ SQLite backend implementation
- ✅ Basic Pydantic models

### Phase 2: Flexibility ✅
- ✅ Multiple backend support (SQLite, DuckDB, DynamoDB)
- ✅ Repository factory with auto-detection
- ✅ YAML configuration management
- ✅ JSON serialization for complex types

### Phase 3: Optimization ✅
- ✅ Reserved keyword handling
- ✅ Context manager resource management
- ✅ Bangkok timezone standardization
- ✅ Comprehensive test coverage

### Phase 4: Production Ready ✅
- ✅ 10 complete data models
- ✅ Cross-backend compatibility
- ✅ Error handling and validation
- ✅ Documentation and examples

### Next Phase: Vector Integration 🚧
- Vector storage implementation
- Semantic search capabilities
- Multi-step filtering system