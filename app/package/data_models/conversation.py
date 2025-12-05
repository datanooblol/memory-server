from pydantic import Field
from uuid import uuid4
from enum import StrEnum
from typing import Optional, List
from .base import BaseTimestampModel

class Role(StrEnum):
    user = "user"
    assistant = "assistant"

class Conversation(BaseTimestampModel):
    convo_id: str = Field(default_factory=lambda: str(uuid4()), description="Primary key - unique conversation identifier")
    chat_session_id: str = Field(description="Foreign key - references ChatSession.chat_session_id")
    role: Role = Field(description="Role of the message sender (user or assistant)")
    content: str = Field(description="Content of the conversation message")
    references: Optional[List[str]] = Field(default=None, description="Optional list of reference IDs")