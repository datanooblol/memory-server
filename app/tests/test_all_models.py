import asyncio
from package.storage.manager import StorageManager
from package.repositories.factory import RepositoryFactory
from package.schemas import TABLE_SCHEMAS
from package.data_models.user import User
from package.data_models.project import Project
from package.data_models.chat_session import ChatSession
from package.data_models.conversation import Conversation, Role
from package.data_models.source import Source, SourceType

async def test_all_models(backend_name: str):
    print(f"=== Testing All Models with {backend_name} ===")
    
    # Initialize storage
    storage_manager = StorageManager("config/storage.yaml")
    storage = storage_manager.get_relational(backend_name)
    
    # Create all tables
    print("Creating tables...")
    for table_name, schema in TABLE_SCHEMAS.items():
        await storage.create_table(table_name, schema)
    print("Tables created successfully!")
    
    repo_factory = RepositoryFactory(storage)
    
    # Test User
    print("\n--- Testing User ---")
    user_repo = repo_factory.get_user_repository()
    user = User(email="test@example.com", password="hashed_password")
    user_id = await user_repo.create(user)
    print(f"Created user: {user_id}")
    
    found_user = await user_repo.get_by_id(user_id)
    print(f"Found user: {found_user.email}")
    
    # Test Project
    print("\n--- Testing Project ---")
    project_repo = repo_factory.get_project_repository()
    project = Project(
        user_id=user_id, 
        project_name="Test Project", 
        project_description="A test project for demo"
    )
    project_id = await project_repo.create(project)
    print(f"Created project: {project_id}")
    
    found_project = await project_repo.get_by_id(project_id)
    print(f"Found project: {found_project.project_name}")
    
    # Test ChatSession
    print("\n--- Testing ChatSession ---")
    session_repo = repo_factory.get_chat_session_repository()
    session = ChatSession(project_id=project_id, session_name="Test Session")
    session_id = await session_repo.create(session)
    print(f"Created chat session: {session_id}")
    
    found_session = await session_repo.get_by_id(session_id)
    print(f"Found session: {found_session.session_name}")
    
    # Test Conversation
    print("\n--- Testing Conversation ---")
    convo_repo = repo_factory.get_conversation_repository()
    conversation = Conversation(
        chat_session_id=session_id,
        role=Role.user,
        content="Hello, this is a test message",
        references=["ref1", "ref2"]  # Test list serialization
    )
    convo_id = await convo_repo.create(conversation)
    print(f"Created conversation: {convo_id}")
    
    found_convo = await convo_repo.get_by_id(convo_id)
    print(f"Found conversation: {found_convo.content}")
    print(f"References: {found_convo.references}")
    
    # Test Source
    print("\n--- Testing Source ---")
    source_repo = repo_factory.get_source_repository()
    source = Source(
        project_id=project_id,
        source_name="test_data.csv",
        size=1024,
        source_type=SourceType.csv,
        source_path={"local_path": "/data/test.csv", "bucket": "my-bucket"}  # Test dict serialization
    )
    source_id = await source_repo.create(source)
    print(f"Created source: {source_id}")
    
    found_source = await source_repo.get_by_id(source_id)
    print(f"Found source: {found_source.source_name}")
    print(f"Source path: {found_source.source_path}")
    
    # Test relationships
    print("\n--- Testing Relationships ---")
    user_projects = await project_repo.find_by({"user_id": user_id})
    print(f"User has {len(user_projects)} projects")
    
    project_sessions = await session_repo.find_by({"project_id": project_id})
    print(f"Project has {len(project_sessions)} chat sessions")
    
    print(f"\n=== All tests completed successfully for {backend_name}! ===")

async def main():
    backends = ["user_data_sqlite", "user_data_duckdb"]
    
    for backend in backends:
        try:
            await test_all_models(backend)
            print(f"\n{'='*50}\n")
        except Exception as e:
            print(f"Error with {backend}: {e}")
            import traceback
            traceback.print_exc()
            print(f"\n{'='*50}\n")

if __name__ == "__main__":
    asyncio.run(main())