from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from package.auth.jwt_auth import verify_token
from package.data_models import ChatSession, Conversation
from package.routers.dependencies import get_chat_session_repo, get_conversation_repo

router = APIRouter(prefix="/conversation", tags=["conversation"])

class ChatSessionRequest(BaseModel):
    content:str

