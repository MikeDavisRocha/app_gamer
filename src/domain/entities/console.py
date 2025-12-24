from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Console:
    id: Optional[int]
    name: str
    company: str
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    deleted_at: Optional[datetime] = None # Soft Delete: Se tiver data, está deletado