from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from package.auth.jwt_auth import verify_token
from package.data_models import ChatSession, Conversation, Role
from package.routers.dependencies import get_chat_session_repo, get_conversation_repo

router = APIRouter(prefix="/conversation", tags=["conversation"])

class ConversationRequest(BaseModel):
    content:str
    role:Role

@router.get("/chat-session/{chat_session_id}")
async def get_conversations(
    chat_session_id:str,
    user_id:str = Depends(verify_token),
    conversation_repo = Depends(get_conversation_repo)
):
    convos = await conversation_repo.find_by(dict(chat_session_id=chat_session_id))
    return {"conversations": convos}

@router.post("/chat-session/{chat_session_id}")
async def create_conversation(
    chat_session_id:str,
    conversation_data:ConversationRequest,
    user_id:str = Depends(verify_token),
    chat_session_repo = Depends(get_chat_session_repo),
    conversation_repo = Depends(get_conversation_repo)
): 
    chat_session = await chat_session_repo.get_by_id(chat_session_id)
    if not chat_session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    new_convo = Conversation(
        chat_session_id=chat_session_id,
        role=conversation_data.role,
        content=conversation_data.content
    )
    convo_id = await conversation_repo.create(new_convo)
    return {"message": f"{conversation_data.role.upper()} conversation created", "convo_id": convo_id}

@router.get("/{convo_id}")
async def get_conversation(
    convo_id:str,
    user_id:str = Depends(verify_token),
    conversation_repo = Depends(get_conversation_repo)
):
    convo = await conversation_repo.get_by_id(convo_id)
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"conversation": convo}

@router.put("/{convo_id}")
async def update_conversation(
    convo_id:str,
    conversation_data:ConversationRequest,
    user_id:str = Depends(verify_token),
    conversation_repo = Depends(get_conversation_repo)
):
    convo = await conversation_repo.get_by_id(convo_id)
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    convo.content = conversation_data.content
    convo.role = conversation_data.role
    await conversation_repo.update(convo)
    return {"message": "Conversation updated"}

@router.delete("/{convo_id}")
async def delete_conversation(
    convo_id:str,
    user_id:str = Depends(verify_token),
    conversation_repo = Depends(get_conversation_repo)
):
    convo = await conversation_repo.get_by_id(convo_id)
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    await conversation_repo.delete(convo_id)
    return {"message": "Conversation deleted"}

# save assistant conversation, but we must add it first then works with two below


# save reference by convo_id

# save agent execution by convo_id