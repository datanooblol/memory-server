from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from package.auth.jwt_auth import verify_token
from package.data_models import ChatSession
from package.routers.dependencies import get_project_repo, get_chat_session_repo

router = APIRouter(prefix="/chat-session", tags=["chat-session"])

class ChatSessionRequest(BaseModel):
    chat_session_id:str
    session_name:str

@router.post("/project/{project_id}")
async def create_chat_session(
    project_id: str,
    chat_session_data: ChatSessionRequest,
    user_id: str = Depends(verify_token),
    project_repo = Depends(get_project_repo),
    chat_session_repo = Depends(get_chat_session_repo)
):
    project = await project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    new_chat_session = ChatSession(
        project_id=project_id,
        session_name=chat_session_data.session_name,
    )
    chat_session_id = await chat_session_repo.create(new_chat_session)
    return {"message": "Chat session created", "chat_session_id": chat_session_id}

@router.get("/project/{project_id}")
async def get_chat_sessions_by_project(
    project_id: str,
    user_id: str = Depends(verify_token),
    chat_session_repo = Depends(get_chat_session_repo)
):
    chat_sessions = await chat_session_repo.find_by(dict(project_id=project_id))
    return {"chat_sessions": chat_sessions}

@router.get("/{chat_session_id}")
async def get_chat_session(
    chat_session_id: str,
    user_id: str = Depends(verify_token),
    chat_session_repo = Depends(get_chat_session_repo)
):
    chat_session = await chat_session_repo.get_by_id(chat_session_id)
    if not chat_session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return {"chat_session": chat_session}

@router.patch("/session-name/{chat_session_id}")
async def update_chat_session_name(
    chat_session_id: str,
    session_name:str,
    user_id: str = Depends(verify_token),
    chat_session_repo = Depends(get_chat_session_repo)
):
    chat_session = await chat_session_repo.get_by_id(chat_session_id)
    if not chat_session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    await chat_session_repo.patch(chat_session_id, dict(session_name=session_name))
    return {"message": "session_name updated successfully"}
    