from pydantic import BaseModel, Field
from datetime import datetime
import pytz

def bangkok_now():
    return datetime.now(pytz.timezone('Asia/Bangkok'))

class BaseTimestampModel(BaseModel):
    created_at: datetime = Field(default_factory=bangkok_now)
    updated_at: datetime = Field(default_factory=bangkok_now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }