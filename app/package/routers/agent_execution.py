from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from package.auth.jwt_auth import verify_token
from package.data_models import AgentExecution, ExecutionStatus
from package.routers.dependencies import get_conversation_repo, get_agent_execution_repo, get_task_repo

router = APIRouter(prefix="/agent-execution", tags=["agent-execution"])

@router.post("/conversation/{convo_id}")
async def create_agent_execution(
    convo_id: str, 
    user_id: str = Depends(verify_token),
    conversation_repo=Depends(get_conversation_repo), 
    agent_execution_repo=Depends(get_agent_execution_repo)
):
    # Check if the conversation exists
    if not conversation_repo.get_by_id(convo_id):
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    new_agent_execution = AgentExecution(convo_id=convo_id)
    agent_execution_id = await agent_execution_repo.create(new_agent_execution)
    return {"message": "Agent execution created", "agent_execution_id": agent_execution_id}


@router.get("/{agent_execution_id}")
async def get_agent_execution(
    agent_execution_id: str,
    user_id: str = Depends(verify_token),
    agent_execution_repo=Depends(get_agent_execution_repo)
):
    agent_execution = await agent_execution_repo.get_by_id(agent_execution_id)
    if not agent_execution:
        raise HTTPException(status_code=404, detail="Agent execution not found")
    return {"agent_execution": agent_execution}

@router.delete("/{agent_execution_id}")
async def delete_agent_execution(
    agent_execution_id: str,
    user_id: str = Depends(verify_token),
    agent_execution_repo=Depends(get_agent_execution_repo)
):
    if not agent_execution_repo.get_by_id(agent_execution_id):
        raise HTTPException(status_code=404, detail="Agent execution not found")
    await agent_execution_repo.delete(agent_execution_id)
    return {"message": "Agent execution deleted"}

@router.patch("/{agent_execution_id}/status")
async def update_agent_execution_status(
    agent_execution_id: str,
    status: ExecutionStatus,
    user_id: str = Depends(verify_token),
    agent_execution_repo=Depends(get_agent_execution_repo)
):
    if not agent_execution_repo.get_by_id(agent_execution_id):
        raise HTTPException(status_code=404, detail="Agent execution not found")
    await agent_execution_repo.patch(agent_execution_id, dict(status=status))
    return {"message": f"Execution status updated to {status}"}

@router.patch("/{agent_execution_id}/tasks-count")
async def update_agent_execution_tasks_count(
    agent_execution_id: str,
    user_id: str = Depends(verify_token),
    task_repo=Depends(get_task_repo),
    agent_execution_repo=Depends(get_agent_execution_repo)
):
    if not agent_execution_repo.get_by_id(agent_execution_id):
        raise HTTPException(status_code=404, detail="Agent execution not found")
    tasks = await task_repo.find_by(dict(execution_id=agent_execution_id))
    await agent_execution_repo.patch(agent_execution_id, dict(total_tasks=len(tasks)))
    return {"message": f"Execution total tasks updated to {len(tasks)}"}
