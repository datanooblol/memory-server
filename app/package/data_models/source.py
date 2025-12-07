from pydantic import Field
from uuid import uuid4
from enum import StrEnum
from typing import Dict, Any
from .base import BaseTimestampModel

class SourceType(StrEnum):
    CSV = "csv"

class SourceStatus(StrEnum):
    PROCESSING = "processing"
    READY = "ready"
    ERROR = "error"

class Source(BaseTimestampModel):
    source_id: str = Field(default_factory=lambda: str(uuid4()), description="Primary key - unique source identifier")
    project_id: str = Field(description="Foreign key - references Project.project_id")
    source_name: str = Field(description="Name of the source file")
    size: int = Field(default=0, description="Size of the source file in bytes")
    source_type: SourceType = Field(description="Type of the source file (csv)")
    status:SourceStatus = Field(default=SourceStatus.PROCESSING, description="Source status")
    is_selected:bool = Field(default=False, description="This source will be used in analytics or not")
    source_path: Dict[str, Any] = Field(description="Path information for the source file")