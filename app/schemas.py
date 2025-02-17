from pydantic import BaseModel
from uuid import UUID
from typing import Optional, Any
from datetime import datetime

class JobResponse(BaseModel):
    job_id: UUID
    status: str
    result: Optional[Any] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        
class JobIdResponse(BaseModel):
    job_id: UUID