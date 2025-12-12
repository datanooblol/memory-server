from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from package.auth.jwt_auth import verify_token
from package.data_models import ChatSession, Conversation, Role, ReferenceData
from package.routers.dependencies import get_chat_session_repo, get_conversation_repo
from typing import List, Optional

router = APIRouter(prefix="/conversation", tags=["conversation"])

class ConversationRequest(BaseModel):
    content:str
    role:Role
    references:Optional[List[ReferenceData]] = None

class ConversationResponse(BaseModel):
    convo_id:str
    role:Role

@router.get("/chat-session/{chat_session_id}", response_model=list[Conversation])
async def get_conversations_by_chat_session(
    chat_session_id:str,
    user_id:str = Depends(verify_token),
    conversation_repo = Depends(get_conversation_repo)
):
    convos = await conversation_repo.find_by(dict(chat_session_id=chat_session_id))
    return convos

@router.post("/chat-session/{chat_session_id}", response_model=ConversationResponse)
async def create_conversation_by_chat_session(
    chat_session_id:str,
    conversation_data:ConversationRequest,
    user_id:str = Depends(verify_token),
    chat_session_repo = Depends(get_chat_session_repo),
    conversation_repo = Depends(get_conversation_repo)
): 
    """This will use to both user and assistant conversation"""
    chat_session = await chat_session_repo.get_by_id(chat_session_id)
    if not chat_session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    new_convo = Conversation(
        chat_session_id=chat_session_id,
        role=conversation_data.role,
        content=conversation_data.content,
        references=conversation_data.references
    )
    convo_id = await conversation_repo.create(new_convo)
    return ConversationResponse(convo_id=convo_id, role=conversation_data.role)

@router.get("/{convo_id}", response_model=Conversation)
async def get_conversation(
    convo_id:str,
    user_id:str = Depends(verify_token),
    conversation_repo = Depends(get_conversation_repo)
):
    convo = await conversation_repo.get_by_id(convo_id)
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return convo

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

class ReferenceRequest(BaseModel):
    references:List[ReferenceData]

@router.patch("/{convo_id}/references")
async def update_conversation_references(
    convo_id:str,
    reference_data:ReferenceRequest,
    user_id:str = Depends(verify_token),
    conversation_repo = Depends(get_conversation_repo)
):
    convo = await conversation_repo.get_by_id(convo_id)
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    print(reference_data.references)
    await conversation_repo.patch(convo_id, dict(references=reference_data.references))
    return {"message": "Conversation references updated"}
