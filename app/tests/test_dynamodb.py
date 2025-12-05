import asyncio
from app.package.storage.manager import StorageManager
from app.package.repositories.factory import RepositoryFactory
from app.package.data_models.user import User

# DynamoDB table schema (just partition key)
USER_KEY_SCHEMA = {
    "partition_key": "user_id"
}

async def test_dynamodb_operations():
    print("=== Testing DynamoDB ===")
    
    # Initialize storage
    storage_manager = StorageManager("app/config/storage.yaml")
    storage = storage_manager.get_nosql("user_data_dynamodb")
    
    # Create table
    await storage.create_table("users", USER_KEY_SCHEMA)
    
    # Initialize repository
    repo_factory = RepositoryFactory(storage)
    user_repo = repo_factory.get_user_repository()
    
    # Create user
    user = User(email="dynamodb@example.com", password="hashed_password")
    user_id = await user_repo.create(user)
    print(f"Created user with ID: {user_id}")
    
    # Get user by ID
    found_user = await user_repo.get_by_id(user_id)
    print(f"Found user: {found_user.email}")
    
    # Find users by email
    users = await user_repo.find_by({"email": "dynamodb@example.com"})
    print(f"Found {len(users)} users with email dynamodb@example.com")
    
    return user_id

async def main():
    try:
        dynamodb_user_id = await test_dynamodb_operations()
        print(f"DynamoDB User ID: {dynamodb_user_id}")
        print("DynamoDB backend works with the same repository interface!")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have AWS credentials configured and boto3 installed")

if __name__ == "__main__":
    asyncio.run(main())