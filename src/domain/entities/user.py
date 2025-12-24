from enum import Enum
from dataclasses import dataclass
from datetime import datetime
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
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()