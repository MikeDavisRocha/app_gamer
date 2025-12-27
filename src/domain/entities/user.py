from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


@dataclass
class User:
    id: Optional[int]
    username: str
    email: str
    password_hash: str
    role: UserRole
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)
