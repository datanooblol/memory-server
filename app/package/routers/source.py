from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel, Field
from typing import Dict, Any
from package.auth.jwt_auth import verify_token
from package.data_models import Project, Source, SourceType
from package.routers.dependencies import get_project_repo, get_source_repo
from pathlib import Path


router = APIRouter(prefix="/source", tags=["source"])

class SourcePathRequest(BaseModel):
    """For local mode"""
    source_name: str = Field(description="Name for the source")
    file_path: str = Field(description="Local file path to register")

class SourceRequest(BaseModel):
    source_name: str
    source_type: SourceType
    size: int = 0
    source_path: Dict[str, Any] = Field(default_factory=dict)

class SourceResponse(BaseModel):
    source_id:str

# Create source under project
@router.post("/project/{project_id}", response_model=SourceResponse)
async def create_source_by_project(
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
    return SourceResponse(source_id=source_id)

# List sources by project
@router.get("/project/{project_id}", response_model=list[Source])
async def get_sources_by_project(
    project_id: str,
    user_id: str = Depends(verify_token),
    source_repo = Depends(get_source_repo)
):
    sources = await source_repo.find_by(dict(project_id=project_id))
    return sources

# Get specific source
@router.get("/{source_id}", response_model=Source)
async def get_source(
    source_id: str,
    user_id: str = Depends(verify_token),
    source_repo = Depends(get_source_repo)
):
    source = await source_repo.get_by_id(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source

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
async def update_source_selection(
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

# In source router
@router.get("/project/{project_id}/selected", response_model=list[Source])
async def get_selected_sources(
    project_id: str,
    user_id: str = Depends(verify_token),
    project_repo = Depends(get_project_repo),
    source_repo = Depends(get_source_repo)
):
    # Validate project ownership
    project = await project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Get selected sources
    selected_sources = await source_repo.find_by({
        "project_id": project_id,
        "is_selected": True
    })
    return selected_sources

@router.delete("/{source_id}")
async def delete_source(
    source_id: str,
    user_id: str = Depends(verify_token),
    source_repo = Depends(get_source_repo)
):
    # Check if project exists and belongs to user
    source = await source_repo.get_by_id(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    await source_repo.delete(source_id)
    return {"message": "Source deleted successfully"}

@router.post("/project/{project_id}/upload", response_model=SourceResponse)
async def upload_file(
    project_id: str,
    file: UploadFile = File(...),
    user_id: str = Depends(verify_token),
    project_repo = Depends(get_project_repo),
    source_repo = Depends(get_source_repo)
):
    # Validate project ownership
    project = await project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files supported")
    
    # Create project directory: ./project_dataset/{project_id}/
    project_dir = Path("./project_dataset") / project_id
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # Store file as: ./project_dataset/{project_id}/{filename}.csv
    file_path = project_dir / file.filename
    
    # Save file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Register source with relative path
    new_source = Source(
        project_id=project_id,
        source_name=file.filename,
        size=len(content),
        source_type=SourceType.CSV,
        source_path={
            "stored_path": f"./project_dataset/{project_id}/{file.filename}",
            "original_name": file.filename
        }
    )
    
    source_id = await source_repo.create(new_source)
    return SourceResponse(source_id=source_id)

# @router.post("/project/{project_id}/register-path", response_model=SourceResponse)
# async def register_local_file(
#     project_id: str,
#     path_data: SourcePathRequest,
#     user_id: str = Depends(verify_token),
#     project_repo = Depends(get_project_repo),
#     source_repo = Depends(get_source_repo)
# ):
#     # Validate project ownership
#     project = await project_repo.get_by_id(project_id)
#     if not project:
#         raise HTTPException(status_code=404, detail="Project not found")
#     if project.user_id != user_id:
#         raise HTTPException(status_code=403, detail="Not authorized")
    
#     # Validate file exists
#     file_path = Path(path_data.file_path)
#     if not file_path.exists():
#         raise HTTPException(status_code=400, detail="File path does not exist")
    
#     # Get file info
#     file_size = file_path.stat().st_size
#     file_extension = file_path.suffix.lower().lstrip('.')
    
#     # Validate file type
#     if file_extension not in ['csv']:
#         raise HTTPException(status_code=400, detail="Unsupported file type")
    
#     # Create source
#     new_source = Source(
#         project_id=project_id,
#         source_name=path_data.source_name,
#         size=file_size,
#         source_type=SourceType.CSV,
#         source_path={
#             "local_path": str(file_path.absolute()),
#             "original_name": file_path.name
#         }
#     )
    
#     source_id = await source_repo.create(new_source)
#     return SourceResponse(source_id=source_id)



