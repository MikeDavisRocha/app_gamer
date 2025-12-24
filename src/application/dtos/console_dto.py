from pydantic import BaseModel, Field
from datetime import datetime

class ConsoleCreateInput(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    company: str = Field(..., min_length=2, max_length=100)

class ConsoleOutput(BaseModel):
    id: int
    name: str
    company: str
    created_at: datetime
    
    class Config:
        from_attributes = True