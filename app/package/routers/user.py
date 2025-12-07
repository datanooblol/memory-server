from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import bcrypt
from package.auth.jwt_auth import create_access_token
from package.data_models import User
from package.routers.dependencies import get_user_repo

router = APIRouter(prefix="/user", tags=["user"])

class UserRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
async def register(user: UserRequest, user_repo = Depends(get_user_repo)):
    # Check if user exists
    existing = await user_repo.find_by({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(email=user.email, password=hashed_password)
    await user_repo.create(new_user)
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(user: UserRequest, user_repo = Depends(get_user_repo)):
    users = await user_repo.find_by({"email": user.email})
    if not users or not bcrypt.checkpw(user.password.encode('utf-8'), users[0].password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": users[0].user_id})
    return {"access_token": access_token, "token_type": "bearer"}
