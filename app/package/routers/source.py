from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, Any
from package.auth.jwt_auth import verify_token
from package.data_models import Project, Source, SourceType
from package.routers.dependencies import get_project_repo, get_source_repo

router = APIRouter(prefix="/source", tags=["source"])

# Remove project_id from SourceRequest since it comes from URL
class SourceRequest(BaseModel):
    source_name: str
    source_type: SourceType
    size: int = 0
    source_path: Dict[str, Any] = Field(default_factory=dict)

# Create source under project
@router.post("/project/{project_id}")
async def create_source(
    project_id: str,
    source_data: SourceRequest,
    user_id: str = Depends(verify_token),
    project_repo = Depends(get_project_repo),
    source_repo = Depends(get_source_repo)
):
    project = await project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    new_source = Source(
        project_id=project_id,  # From URL
        source_name=source_data.source_name,
        size=source_data.size,
        source_type=source_data.source_type,
        source_path=source_data.source_path
    )
    source_id = await source_repo.create(new_source)
    return {"message": "Source created", "source_id": source_id}

# List sources by project
@router.get("/project/{project_id}")
async def get_sources_by_project(
    project_id: str,
    user_id: str = Depends(verify_token),
    source_repo = Depends(get_source_repo)
):
    sources = await source_repo.find_by(dict(project_id=project_id))
    return {"sources": sources}

# Get specific source
@router.get("/{source_id}")
async def get_source(
    source_id: str,
    user_id: str = Depends(verify_token),
    source_repo = Depends(get_source_repo)
):
    source = await source_repo.get_by_id(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return {"source": source}

@router.patch("/source-name/{source_id}")
async def update_source_name(
    source_id: str,
    source_name:str,
    user_id: str = Depends(verify_token),
    source_repo = Depends(get_source_repo)
):
    # Check if project exists and belongs to user
    source = await source_repo.get_by_id(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    await source_repo.patch(source_id, dict(source_name=source_name))
    return {"message": "source_name updated successfully"}
    
@router.patch("/selected/{source_id}")
async def update_source_name(
    source_id: str,
    is_selected:bool,
    user_id: str = Depends(verify_token),
    source_repo = Depends(get_source_repo)
):
    # Check if project exists and belongs to user
    source = await source_repo.get_by_id(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    await source_repo.patch(source_id, dict(is_selected=is_selected))
    return {"message": "is_selected updated successfully"}
