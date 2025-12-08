from pydantic import BaseModel, Field
from uuid import uuid4
from enum import StrEnum
from typing import Optional, List, Dict, Any
from .base import BaseTimestampModel
from .reference import ReferenceType

class Role(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"

class ReferenceData(BaseModel):
    reference_id: str = Field(description="Unique identifier for the reference")
    type: ReferenceType = Field(description="Type of reference")

class Conversation(BaseTimestampModel):
    convo_id: str = Field(default_factory=lambda: str(uuid4()), description="Primary key - unique conversation identifier")
    chat_session_id: str = Field(description="Foreign key - references ChatSession.chat_session_id")
    role: Role = Field(description="Role of the message sender (user or assistant)")
    content: str = Field(description="Content of the conversation message")
    references: Optional[List[ReferenceData]] = Field(default=None, description="Optional list of reference type and id")
    # references: Optional[List[str]] = Field(default=None, description="Optional list of reference IDs")