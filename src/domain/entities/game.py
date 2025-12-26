from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Game:
    id: Optional[int]
    name: str
    console_id: int
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    deleted_at: Optional[datetime] = None
