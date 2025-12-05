# Agentic Memory System Plan

## Overview
Framework for agentic memory system that allows users to upload files and perform SQL operations with learning capabilities.

## Storage Architecture

### Relational Database
- **user**: User information (id, password)
- **project**: User projects
- **chat_session**: Multiple sessions per project
- **source**: Uploaded files per project
- **conversation**: Chat history within sessions
- **agent_tasks**: Agent execution tracking for debugging
- **reference**: Store generated artifacts (SQL queries, Plotly visualizations, results)

### Vector Database
- **source_metadata**: File metadata, schema info, field descriptions
- **episode**: Compressed conversation memory (user + assistant turns)
- **query_patterns**: Semantic patterns of successful queries for learning

## Query Pattern Learning

### Pattern Extraction Process
1. User uploads file → stored in `source` + metadata in vector
2. User asks question → generates SQL
3. SQL executes successfully → stored in `reference`
4. Extract semantic pattern from SQL + user question
5. Store pattern embedding in vector for future similarity matching

### Pattern Generation Methods
- **SQL Parser**: Extract structure (aggregation, grouping, filters)
- **LLM Abstraction**: Convert to semantic description
- **Example**: `SELECT region, SUM(revenue) WHERE date...` → `"aggregate numerical by categorical with temporal filter"`

## Future Capabilities
- Database connections
- Multi-modal visualizations
- Schema inference and learning
- Query optimization through pattern matching

## Workflow
1. Upload → Schema detection → Metadata storage
2. Query → Pattern matching → SQL generation → Execution
3. Success → Pattern learning → Reference storage
4. Failure → Debug tracking in agent_tasks