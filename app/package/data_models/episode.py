from pydantic import Field
from uuid import uuid4
from .base import BaseTimestampModel
from typing import List, Optional

class Episode(BaseTimestampModel):
    episode_id: str = Field(default_factory=lambda: str(uuid4()), description="Primary key - unique episode identifier")
    chat_session_id: str = Field(description="Foreign key - references ChatSession.chat_session_id")
    convo_ids: List[str] = Field(default=[], description="List of conversation IDs that make up this episode")
    parent_episode_ids: Optional[List[str]] = Field(default=None, description="Episode IDs that were merged to create this episode")
    episode_name: str = Field(default="", description="Name of the episode")
    episode_summary: str = Field(default="", description="Summary of the episode content")
    level: int = Field(default=1, description="Episode level - 1 for base episodes, 2+ for rollups")
    active: bool = Field(default=True, description="Whether the episode is active or archived")