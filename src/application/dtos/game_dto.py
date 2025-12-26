from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class GameCreateInput(BaseModel):
    name: str = Field(..., min_length=2)
    console_id: int


class GameOutput(BaseModel):
    id: int
    name: str
    console_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# DTO para resposta paginada
class PaginatedGameResponse(BaseModel):
    total: int
    items: List[GameOutput]
    page: int
    size: int
