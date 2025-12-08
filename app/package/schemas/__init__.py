# Compatible schemas for both SQLite and DuckDB
# Using TEXT for all string fields and JSON for complex types

USER = {
    "user_id": "TEXT PRIMARY KEY",
    "email": "TEXT NOT NULL UNIQUE",
    "password": "TEXT NOT NULL",
    "created_at": "TEXT NOT NULL",
    "updated_at": "TEXT NOT NULL"
}

PROJECT = {
    "project_id": "TEXT PRIMARY KEY",
    "user_id": "TEXT NOT NULL",
    "project_name": "TEXT NOT NULL",
    "project_description": "TEXT NOT NULL",
    "created_at": "TEXT NOT NULL",
    "updated_at": "TEXT NOT NULL"
}

CHAT_SESSION = {
    "chat_session_id": "TEXT PRIMARY KEY",
    "project_id": "TEXT NOT NULL",
    "session_name": "TEXT NOT NULL",
    "created_at": "TEXT NOT NULL",
    "updated_at": "TEXT NOT NULL"
}

CONVERSATION = {
    "convo_id": "TEXT PRIMARY KEY",
    "chat_session_id": "TEXT NOT NULL",
    "role": "TEXT NOT NULL",
    "content": "TEXT NOT NULL",
    "references": "TEXT",  # JSON string for list
    "created_at": "TEXT NOT NULL",
    "updated_at": "TEXT NOT NULL"
}

SOURCE = {
    "source_id": "TEXT PRIMARY KEY",
    "project_id": "TEXT NOT NULL",
    "source_name": "TEXT NOT NULL",
    "size": "INTEGER NOT NULL",
    "source_type": "TEXT NOT NULL",
    "status": "TEXT NOT NULL", 
    "is_selected": "TEXT NOT NULL",
    "source_path": "TEXT NOT NULL",  # JSON string for dict
    "created_at": "TEXT NOT NULL",
    "updated_at": "TEXT NOT NULL"
}

REFERENCE = {
    "reference_id": "TEXT PRIMARY KEY",
    "convo_id": "TEXT NOT NULL",
    "type": "TEXT NOT NULL",
    "content": "TEXT NOT NULL",
    "created_at": "TEXT NOT NULL",
    "updated_at": "TEXT NOT NULL"
}

AGENT_EXECUTION = {
    "execution_id": "TEXT PRIMARY KEY",
    "convo_id": "TEXT NOT NULL",
    "status": "TEXT NOT NULL",
    "total_tasks": "INTEGER NOT NULL DEFAULT 0",
    "created_at": "TEXT NOT NULL",
    "updated_at": "TEXT NOT NULL"
}

# Add new TASK schema
TASK = {
    "task_id": "TEXT PRIMARY KEY",
    "execution_id": "TEXT NOT NULL",
    "task_name": "TEXT NOT NULL",
    "status": "TEXT NOT NULL",
    "sequence_order": "INTEGER NOT NULL",
    "input_data": "TEXT NOT NULL",  # JSON string
    "output_data": "TEXT",  # JSON string, nullable
    "error_message": "TEXT",  # nullable
    "model_id": "TEXT",  # nullable
    "input_tokens": "INTEGER",  # nullable
    "output_tokens": "INTEGER",  # nullable
    "cost": "REAL",  # nullable, for decimal values
    "created_at": "TEXT NOT NULL",
    "updated_at": "TEXT NOT NULL"
}

EPISODE = {
    "episode_id": "TEXT PRIMARY KEY",
    "chat_session_id": "TEXT NOT NULL",
    "convo_ids": "TEXT NOT NULL",  # JSON string for list
    "parent_episode_ids": "TEXT",  # JSON string for optional list
    "episode_name": "TEXT NOT NULL",
    "episode_summary": "TEXT NOT NULL",
    "level": "INTEGER NOT NULL",
    "active": "INTEGER NOT NULL",  # 0/1 for boolean
    "created_at": "TEXT NOT NULL",
    "updated_at": "TEXT NOT NULL"
}

# Vector store may varied

METADATA = {
    "metadata_id": "TEXT PRIMARY KEY",
    "source_id": "TEXT NOT NULL",
    "table_name": "TEXT NOT NULL",
    "description": "TEXT NOT NULL",
    "created_at": "TEXT NOT NULL",
    "updated_at": "TEXT NOT NULL"
}

FIELD_METADATA = {
    "field_id": "TEXT PRIMARY KEY",
    "source_id": "TEXT NOT NULL",
    "field_name": "TEXT NOT NULL",
    "data_type": "TEXT NOT NULL",
    "input_type": "TEXT NOT NULL",
    "description": "TEXT NOT NULL",
    "sample_values": "TEXT"  # JSON string for optional list
}

# Table name mapping, but maybe no need
TABLE_SCHEMAS = {
    "users": USER,
    "projects": PROJECT,
    "chat_sessions": CHAT_SESSION,
    "conversations": CONVERSATION,
    "sources": SOURCE,
    "references": REFERENCE,  # Add this if missing
    "agent_executions": AGENT_EXECUTION,
    "tasks": TASK,  # Add new table
    "episodes": EPISODE,
    "metadata": METADATA,
    "field_metadata": FIELD_METADATA
}
