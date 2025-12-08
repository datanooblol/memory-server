from package.repositories.factory import RepositoryFactory
from package.storage.factory import StorageFactory
import package.schemas as schemas

async def get_user_repo():
    storage = StorageFactory.create_relational("duckdb", dict(path="./data/memory.db"))
    await storage.create_table("users", schemas.USER)
    factory = RepositoryFactory(storage)
    return factory.get_user_repository()

async def get_project_repo():
    storage = StorageFactory.create_relational("duckdb", dict(path="./data/memory.db"))
    await storage.create_table("projects", schemas.PROJECT)
    factory = RepositoryFactory(storage)
    return factory.get_project_repository()

async def get_source_repo():
    storage = StorageFactory.create_relational("duckdb", dict(path="./data/memory.db"))
    await storage.create_table("sources", schemas.SOURCE)
    factory = RepositoryFactory(storage)
    return factory.get_source_repository()

async def get_chat_session_repo():
    storage = StorageFactory.create_relational("duckdb", dict(path="./data/memory.db"))
    await storage.create_table("chat_sessions", schemas.CHAT_SESSION)
    factory = RepositoryFactory(storage)
    return factory.get_chat_session_repository()

async def get_conversation_repo():
    storage = StorageFactory.create_relational("duckdb", dict(path="./data/memory.db"))
    await storage.create_table("conversations", schemas.CONVERSATION)
    factory = RepositoryFactory(storage)
    return factory.get_conversation_repository()

async def get_reference_repo():
    storage = StorageFactory.create_relational("duckdb", dict(path="./data/memory.db"))
    await storage.create_table("references", schemas.REFERENCE)
    factory = RepositoryFactory(storage)
    return factory.get_reference_repository()

async def get_agent_execution_repo():
    storage = StorageFactory.create_relational("duckdb", dict(path="./data/memory.db"))
    await storage.create_table("agent_executions", schemas.AGENT_EXECUTION)
    factory = RepositoryFactory(storage)
    return factory.get_agent_execution_repository()

async def get_task_repo():
    storage = StorageFactory.create_relational("duckdb", dict(path="./data/memory.db"))
    await storage.create_table("tasks", schemas.TASK)
    factory = RepositoryFactory(storage)
    return factory.get_task_repository()

async def get_metadata_repo():
    storage = StorageFactory.create_relational("duckdb", dict(path="./data/memory.db"))
    await storage.create_table("metadata", schemas.METADATA)
    factory = RepositoryFactory(storage)
    return factory.get_metadata_repository()

async def get_field_metadata_repo():
    storage = StorageFactory.create_relational("duckdb", dict(path="./data/memory.db"))
    await storage.create_table("field_metadata", schemas.FIELD_METADATA)
    factory = RepositoryFactory(storage)
    return factory.get_field_metadata_repository()