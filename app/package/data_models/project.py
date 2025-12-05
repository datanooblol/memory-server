from pydantic import Field
from uuid import uuid4
from .base import BaseTimestampModel

class Project(BaseTimestampModel):
    project_id: str = Field(default_factory=lambda: str(uuid4()), description="Primary key - unique project identifier")
    user_id: str = Field(description="Foreign key - references User.user_id")
    project_name: str = Field(description="Name of the project")
    project_description: str = Field(description="Description of the project")