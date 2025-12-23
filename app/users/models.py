from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    id: int
    email: str
    password_hash: Optional[str]
    auth_provider: str
    provider_id: Optional[str]
    role: str
    is_active: bool
    created_at: datetime
