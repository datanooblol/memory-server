from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from package.auth.jwt_auth import verify_token
from package.data_models import Project
from package.routers.dependencies import get_project_repo

router = APIRouter(prefix="/project", tags=["project"])

class ProjectRequest(BaseModel):
    project_name:str
    project_description:str

class ProjectResponse(BaseModel):
    project_id:str

@router.post("", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectRequest,
    user_id: str = Depends(verify_token),
    project_repo = Depends(get_project_repo)
):
    new_project = Project(
        user_id=user_id,
        project_name=project_data.project_name,
        project_description=project_data.project_description
    )
    
    project_id = await project_repo.create(new_project)
    return ProjectResponse(project_id=project_id)

@router.get("", response_model=list[Project])
async def get_all_projects(
    user_id: str = Depends(verify_token),
    project_repo = Depends(get_project_repo)
):
    projects = await project_repo.find_by(dict(user_id=user_id))
    return projects

@router.get("/{project_id}", response_model=Project)
async def get_project(
    project_id:str,
    user_id: str = Depends(verify_token),
    project_repo = Depends(get_project_repo)
):
    project = await project_repo.get_by_id(project_id)
    return project

@router.put("/{project_id}")
async def update_project(
    project_id: str,
    project_data: ProjectRequest,
    user_id: str = Depends(verify_token),
    project_repo = Depends(get_project_repo)
):
    # Check if project exists and belongs to user
    project = await project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Update project
    updated_project = Project(
        project_id=project_id,
        user_id=user_id,
        project_name=project_data.project_name,
        project_description=project_data.project_description
    )
    await project_repo.update(project_id, updated_project)
    return {"message": "Project updated"}

@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    user_id: str = Depends(verify_token),
    project_repo = Depends(get_project_repo)
):
    # Check if project exists and belongs to user
    project = await project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Delete project
    await project_repo.delete(project_id)
    return {"message": "Project deleted"}
