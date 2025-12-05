# Storage Factory Design

## Overview
Plug-and-play storage architecture allowing mix-and-match of different storage backends through configuration without code changes.

## Architecture

### Interface Layer
- `RelationalStorage` - Abstract interface for SQL-like operations
- `VectorStorage` - Abstract interface for embedding operations

### Implementation Layer
- `SQLiteStorage` - SQLite implementation
- `DuckDBStorage` - DuckDB implementation  
- `ChromaStorage` - ChromaDB implementation
- `QdrantStorage` - Qdrant implementation (future)

### Factory Layer
- `StorageFactory` - Creates storage instances based on type
- `StorageManager` - Manages multiple storage instances from config

## Configuration-Driven Setup

```yaml
relational:
  user_data:
    type: "sqlite"
    config: {path: "users.db"}
  project_data:
    type: "duckdb"
    config: {path: "projects.duckdb"}

vector:
  metadata:
    type: "chroma"
    config: {path: "./chroma_metadata"}
  episodes:
    type: "qdrant"
    config: {url: "localhost:6333"}
```

## Usage Pattern

```python
storage = StorageManager("config/storage.yaml")

# Different backends for different data types
user_db = storage.get_relational("user_data")      # SQLite
project_db = storage.get_relational("project_data") # DuckDB
metadata_vec = storage.get_vector("metadata")       # Chroma
episodes_vec = storage.get_vector("episodes")       # Qdrant
```

## Benefits

- **Flexibility**: Switch storage backends per data type
- **Testing**: Use in-memory stores for tests, production stores for deployment
- **Performance**: Optimize each data type with appropriate storage
- **Migration**: Gradual migration between storage systems
- **Experimentation**: Easy A/B testing of storage solutions

## File Structure

```
storage/
├── interfaces.py      # Abstract base classes
├── sqlite_storage.py  # SQLite implementation
├── duckdb_storage.py  # DuckDB implementation
├── chroma_storage.py  # ChromaDB implementation
├── factory.py         # Storage factory
└── manager.py         # Storage manager

config/
└── storage.yaml       # Storage configuration
```

## Adding New Storage Backend

1. Implement the interface (`RelationalStorage` or `VectorStorage`)
2. Add to factory's create method
3. Update config file
4. No existing code changes needed