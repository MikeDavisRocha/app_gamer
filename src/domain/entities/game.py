from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

@dataclass
class Game:
    id: Optional[int]
    name: str
    console_id: int
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)
    deleted_at: Optional[datetime] = None
