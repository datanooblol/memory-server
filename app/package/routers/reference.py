from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from package.auth.jwt_auth import verify_token
from package.data_models import ReferenceData, Reference, ReferenceType
from package.routers.dependencies import get_conversation_repo, get_reference_repo

router = APIRouter(prefix="/reference", tags=["reference"])

class ReferenceRequest(BaseModel):
    type:ReferenceType
    content:str

class ReferenceResponse(BaseModel):
    reference_id:str
    type:ReferenceType

@router.post("/conversation/{convo_id}", response_model=ReferenceResponse)
async def create_reference(
    convo_id:str,
    reference_data:ReferenceRequest,
    user_id:str = Depends(verify_token),
    conversation_repo = Depends(get_conversation_repo),
    reference_repo = Depends(get_reference_repo)
):
    convo = await conversation_repo.get_by_id(convo_id)
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    new_reference = Reference(
        convo_id=convo_id,
        type=reference_data.type,
        content=reference_data.content
    )
    reference_id = await reference_repo.create(new_reference)
    return ReferenceResponse(reference_id=reference_id, type=reference_data.type)

@router.get("/{reference_id}", response_model=Reference)
async def get_reference(
    reference_id:str,
    user_id:str = Depends(verify_token),
    reference_repo = Depends(get_reference_repo)
):
    reference = await reference_repo.get_by_id(reference_id)
    if not reference:
        raise HTTPException(status_code=404, detail="Reference not found")
    return reference

@router.put("/{reference_id}")
async def update_reference(
    reference_id:str,
    reference_data:ReferenceRequest,
    user_id:str = Depends(verify_token),
    reference_repo = Depends(get_reference_repo)
):
    reference = await reference_repo.get_by_id(reference_id)
    if not reference:
        raise HTTPException(status_code=404, detail="Reference not found")
    reference.content = reference_data.content
    reference.type = reference_data.type
    await reference_repo.update(reference_id, reference)
    return {"message": "Reference updated"}

@router.delete("/{reference_id}")
async def delete_reference(
    reference_id:str,
    user_id:str = Depends(verify_token),
    reference_repo = Depends(get_reference_repo)
):
    reference = await reference_repo.get_by_id(reference_id)
    if not reference:
        raise HTTPException(status_code=404, detail="Reference not found")
    await reference_repo.delete(reference_id)
    return {"message": "Reference deleted"}

@router.get("/conversation/{convo_id}", response_model=list[Reference])
async def get_references_by_conversation(
    convo_id:str,
    user_id:str = Depends(verify_token),
    reference_repo = Depends(get_reference_repo)
):
    references = await reference_repo.find_by(dict(convo_id=convo_id))
    return references

# @router.patch("/conversation/{convo_id}")
# async def update_references_by_conversation(
#     convo_id:str,
#     user_id:str = Depends(verify_token),
#     conversation_repo = Depends(get_conversation_repo),
#     reference_repo = Depends(get_reference_repo)
# ):
#     convo = await conversation_repo.get_by_id(convo_id)
#     if not convo:
#         raise HTTPException(status_code=404, detail="Conversation not found")
#     references = await reference_repo.find_by(dict(convo_id=convo_id))
#     if not references:
#         raise HTTPException(status_code=404, detail="References not found")
#     new_references = [ReferenceData(reference_id=r.reference_id, type=r.type) for r in references]
#     # convo.references = new_references
#     await conversation_repo.patch(convo_id, dict(references=new_references))
#     return {"message": "Conversation's references updated"}