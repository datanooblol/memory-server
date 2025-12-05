from pydantic import Field
from uuid import uuid4
from typing import List, Dict, Any, Optional
from .base import BaseTimestampModel

class AgentExecution(BaseTimestampModel):
    execution_id: str = Field(default_factory=lambda: str(uuid4()), description="Primary key - unique agent execution identifier")
    convo_id: str = Field(description="Foreign key - references Conversation.convo_id")
    tasks: List[Dict[str, Any]] = Field(description="List of tasks and steps the agent performed during execution")