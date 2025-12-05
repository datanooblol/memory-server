# Agentic Memory System Plan

## Overview
Framework for agentic memory system that allows users to upload files and perform SQL operations with learning capabilities.

## Implemented Storage Architecture

### Relational Database (IMPLEMENTED)
- **user**: User information (id, email, password) with Bangkok timezone
- **project**: User projects with descriptions
- **chat_session**: Multiple sessions per project
- **source**: Uploaded files with metadata and path information
- **conversation**: Chat history with role-based messages and references
- **agent_execution**: Agent task tracking with execution steps (replaces agent_tasks)
- **episode**: Compressed conversation memory with hierarchical rollups
- **metadata**: Table-level metadata for semantic search
- **field_metadata**: Field-level metadata with sample values for enhanced search

### Vector Database (PLANNED)
- **source_metadata**: File metadata embeddings for semantic search
- **episode**: Compressed conversation embeddings
- **query_patterns**: Semantic patterns of successful queries for learning

## Current Implementation Status

### ✅ Completed
- **Multi-backend Storage**: SQLite, DuckDB, DynamoDB support
- **Repository Pattern**: Generic CRUD operations with automatic backend detection
- **Data Models**: 10 Pydantic models with validation and Bangkok timezone
- **Schema Management**: Cross-compatible SQL schemas with JSON serialization
- **Complex Data Types**: Automatic JSON serialization for lists, dicts, booleans
- **Reserved Keyword Handling**: Proper SQL escaping for column names
- **Configuration-Driven**: YAML-based storage backend selection

### 🚧 In Progress
- Vector storage implementation
- Semantic search capabilities
- Query pattern learning

### 📋 Planned
- File upload and processing
- SQL generation from natural language
- Visualization generation
- Database connections
- Multi-step semantic filtering

## Data Model Relationships
```
User (1) → (N) Project
Project (1) → (N) ChatSession
Project (1) → (N) Source
ChatSession (1) → (N) Conversation
Conversation (1) → (N) AgentExecution
ChatSession (1) → (N) Episode
Source (1) → (1) Metadata
Metadata (1) → (N) FieldMetadata
```

## Storage Backend Flexibility
- **SQLite**: Development and testing
- **DuckDB**: Analytics and large datasets
- **DynamoDB**: Cloud-native NoSQL
- **Future**: PostgreSQL, MongoDB, etc.

## Workflow (Current)
1. User creates account → User table
2. User creates project → Project table
3. User starts chat → ChatSession table
4. User/Assistant exchange → Conversation table
5. Agent processes → AgentExecution table
6. Conversations compress → Episode table
7. Files upload → Source + Metadata + FieldMetadata tables