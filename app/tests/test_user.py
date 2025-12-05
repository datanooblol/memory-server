import asyncio
from app.package.storage.manager import StorageManager
from app.package.repositories.factory import RepositoryFactory
from app.package.data_models.user import User

# User table schema
USER_SCHEMA = {
    "user_id": "TEXT PRIMARY KEY",
    "email": "TEXT NOT NULL UNIQUE",
    "password": "TEXT NOT NULL",
    "created_at": "TEXT NOT NULL",
    "updated_at": "TEXT NOT NULL"
}

async def test_user_operations(backend_name: str):
    print(f"\n=== Testing {backend_name} ===")
    
    # Initialize storage
    storage_manager = StorageManager("app/config/storage.yaml")
    storage = storage_manager.get_relational(backend_name)
    
    # Create table
    await storage.create_table("users", USER_SCHEMA)
    
    # Initialize repository
    repo_factory = RepositoryFactory(storage)
    user_repo = repo_factory.get_user_repository()
    
    # Create user
    user = User(email="test@example.com", password="hashed_password")
    user_id = await user_repo.create(user)
    print(f"Created user with ID: {user_id}")
    
    # Get user by ID
    found_user = await user_repo.get_by_id(user_id)
    print(f"Found user: {found_user.email}")
    
    # Find users by email
    users = await user_repo.find_by({"email": "test@example.com"})
    print(f"Found {len(users)} users with email test@example.com")
    
    return user_id

async def main():
    # Test SQLite
    sqlite_user_id = await test_user_operations("user_data_sqlite")
    
    # Test DuckDB
    duckdb_user_id = await test_user_operations("user_data_duckdb")
    
    print(f"\nSQLite User ID: {sqlite_user_id}")
    print(f"DuckDB User ID: {duckdb_user_id}")
    print("Both backends work with the same code!")

if __name__ == "__main__":
    asyncio.run(main())