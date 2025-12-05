from pydantic import Field
from uuid import uuid4
from enum import StrEnum
from .base import BaseTimestampModel

class ReferenceType(StrEnum):
    sql_code = "sql_code"
    sql_data = "sql_data"
    plotly_code = "plotly_code"
    plotly_data = "plotly_data"

class Reference(BaseTimestampModel):
    reference_id: str = Field(default_factory=lambda: str(uuid4()), description="Primary key - unique reference identifier")
    convo_id: str = Field(description="Foreign key - references Conversation.convo_id")
    type: ReferenceType = Field(description="Type of reference (sql_code, sql_data, plotly_code, plotly_data)")
    content: str = Field(description="Content of the reference")