from pydantic import Field
from uuid import uuid4
from .base import BaseTimestampModel

class ChatSession(BaseTimestampModel):
    chat_session_id: str = Field(default_factory=lambda: str(uuid4()), description="Primary key - unique chat session identifier")
    project_id: str = Field(description="Foreign key - references Project.project_id")
    session_name: str = Field(default="", description="Name of the chat session")