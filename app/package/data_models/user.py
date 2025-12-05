from pydantic import Field
from uuid import uuid4
from .base import BaseTimestampModel

class User(BaseTimestampModel):
    user_id: str = Field(default_factory=lambda: str(uuid4()), description="Primary key - unique user identifier")
    email: str = Field(description="User email address")
    password: str = Field(description="Hashed password")
