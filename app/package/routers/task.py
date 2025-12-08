from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from package.auth.jwt_auth import verify_token
from package.data_models import Task, TaskName, TaskStatus
from package.routers.dependencies import get_agent_execution_repo, get_task_repo

router = APIRouter(prefix="/task", tags=["task"])

class TaskRequest(BaseModel):
    task_name: TaskName = Field(description="Type of task being executed")
    status: TaskStatus = Field(description="Status of the task")
    input_data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Input parameters and data for the task")
    output_data: Optional[Dict[str, Any]] = Field(default=None, description="Results and output data from task execution")
    error_message: Optional[str] = Field(default=None, description="Error message if task failed")
    model_id: Optional[str] = Field(default=None, description="LLM model used for this task (e.g., 'gpt-4', 'claude-3')")
    input_tokens: Optional[int] = Field(default=None, description="Number of input tokens consumed")
    output_tokens: Optional[int] = Field(default=None, description="Number of output tokens generated")
    cost: Optional[float] = Field(default=None, description="Cost of this task execution in USD")

@router.post("/agent-execution/{agent_execution_id}")
async def create_task(
    agent_execution_id:str,
    task_data:TaskRequest,
    user_id: str = Depends(verify_token),
    agent_execution_repo=Depends(get_agent_execution_repo),
    task_repo=Depends(get_task_repo)
):
    if not agent_execution_repo.get_by_id(agent_execution_id):
        raise HTTPException(status_code=404, detail="Agent execution not found")
    tasks = await task_repo.find_by(dict(execution_id=agent_execution_id))
    new_task = Task(
        execution_id=agent_execution_id,
        task_name=task_data.task_name,
        status=task_data.status,
        sequence_order=len(tasks)+1,
        input_data=task_data.input_data,
        output_data=task_data.output_data,
        error_message=task_data.error_message,
        model_id=task_data.model_id,
        input_tokens=task_data.input_tokens,
        output_tokens=task_data.output_tokens,
        cost=task_data.cost
    )
    task_id = await task_repo.create(new_task)
    return {"message": "Task created", "task_id": task_id}

# Get specific task
@router.get("/{task_id}")
async def get_task(
    task_id: str,
    user_id: str = Depends(verify_token),
    task_repo = Depends(get_task_repo)
):
    task = await task_repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task": task}

# List tasks for execution (ordered by sequence)
@router.get("/agent-execution/{agent_execution_id}")
async def get_tasks_by_execution(
    agent_execution_id: str,
    user_id: str = Depends(verify_token),
    task_repo = Depends(get_task_repo)
):
    tasks = await task_repo.find_by(dict(execution_id= agent_execution_id), order_by="sequence_order")
    return {"tasks": tasks}

# Delete task (optional)
@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    user_id: str = Depends(verify_token),
    task_repo = Depends(get_task_repo)
):
    task = await task_repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await task_repo.delete(task_id)
    return {"message": "Task deleted"}
