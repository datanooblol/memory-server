from pydantic import Field
from uuid import uuid4
from typing import Dict, Any, Optional
from .base import BaseTimestampModel
from enum import StrEnum

class TaskStatus(StrEnum):
    PENDING = "pending"        # Created but not started
    IN_PROGRESS = "in_progress"  # Currently running
    SUCCESS = "success"        # Completed successfully
    FAILED = "failed"         # Failed with error
    CANCELLED = "cancelled"   # Manually cancelled
    TIMEOUT = "timeout"       # Exceeded time limit
    SKIPPED = "skipped"       # Skipped due to a condition
    RETRYING = "retrying"     # Retrying due to failure

class TaskName(StrEnum):
    VALIDATE_SESSION = "validate_session"
    LOAD_CONTEXT = "load_context"
    GENERATE_SQL = "generate_sql"
    EXECUTE_QUERY = "execute_query"
    GENERATE_CHART = "generate_chart"
    GENERATE_RESPONSE = "generate_response"
    SAVE_MESSAGE = "save_message"

class Task(BaseTimestampModel):
    # Identity
    task_id: str = Field(default_factory=lambda: str(uuid4()))
    execution_id: str = Field(description="Foreign key - references AgentExecution")
    task_name: TaskName = Field(description="Name of the task (e.g., 'generate_response', 'tool_call')")
    
    # Status & Order
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    sequence_order: int = Field(description="Order of task in execution")
    
    # Data
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    
    # LLM Tracking
    model_id: Optional[str] = Field(description="Model used (e.g., 'gpt-4', 'claude-3')")
    input_tokens: Optional[int] = Field(description="Input tokens for this model")
    output_tokens: Optional[int] = Field(description="Output tokens for this model")
    cost: Optional[float] = Field(description="Cost for this task in USD")
