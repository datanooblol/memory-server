from pydantic import BaseModel, Field
from uuid import uuid4
from enum import Enum
from typing import List, Dict, Any, Optional
from .base import BaseTimestampModel

class InputType(str, Enum):
    ID = "id"
    INPUT = "input"
    REJECT = "reject"

class FieldMetadata(BaseTimestampModel):
    field_id: str = Field(default_factory=lambda: str(uuid4()), description="Primary key - unique field identifier")
    source_id: str = Field(description="Foreign key - references Source.source_id")
    field_name: str = Field(description="Name of the field/column")
    data_type: str = Field(description="Data type of the field (extracted from CSV)")
    input_type: InputType = Field(default=InputType.INPUT,description="How this field should be treated (id, input, reject)")
    description: str = Field(default="", description="Description of the field")
    sample_values: Optional[List[str]] = Field(default=None, description="Sample values for better context understanding")
    
    def get_embedding_text(self) -> str:
        """Generate text for vector embedding"""
        parts = [
            f"Field: {self.field_name}",
            f"Type: {self.data_type}",
            f"Description: {self.description}"
        ]
        
        if self.sample_values:
            sample_text = ", ".join(self.sample_values[:5])
            parts.append(f"Examples: {sample_text}")
        
        return " | ".join(parts)

class Metadata(BaseTimestampModel):
    metadata_id: str = Field(default_factory=lambda: str(uuid4()), description="Primary key - unique metadata identifier")
    source_id: str = Field(description="Foreign key - references Source.source_id")
    table_name: str = Field(description="Table name (derived from filename)")
    description: str = Field(default="", description="User-provided description of the dataset")
    
    def get_embedding_text(self) -> str:
        """Generate text for vector embedding"""
        parts = [
            f"Table: {self.table_name}",
            f"Description: {self.description}"
        ]
        
        return " | ".join(parts)

"""
Note:
- This will be used and multi-step filtering
- 1st step using user input to find the tables with high similarity
- 2nd when we have candidated tables, user input will be used to find the field_name and description with high similarity
- 3rd then pack them as metadata context with user input for generating SQL
"""