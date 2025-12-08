from pydantic import Field
from uuid import uuid4
from typing import List, Dict, Any, Optional
from .base import BaseTimestampModel
from enum import StrEnum

class ExecutionStatus(StrEnum):
    PENDING = "pending"        # Created but not started
    IN_PROGRESS = "in_progress"  # Currently running
    SUCCESS = "success"        # Completed successfully
    FAILED = "failed"         # Failed with error
    CANCELLED = "cancelled"   # Manually cancelled
    TIMEOUT = "timeout"       # Exceeded time limit

class AgentExecution(BaseTimestampModel):
    execution_id: str = Field(default_factory=lambda: str(uuid4()), description="Primary key - unique agent execution identifier")
    convo_id: str = Field(description="Foreign key - references Conversation.convo_id")
    status: ExecutionStatus = Field(default=ExecutionStatus.PENDING, description="Status of the agent execution")
    total_tasks: Optional[int] = Field(default=0, description="Total number of tasks the agent is expected to perform")

