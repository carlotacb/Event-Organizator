import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: uuid.UUID
    email: str
    password: str
    first_name: str
    last_name: str
    username: str
    bio: str
    profile_image: str
    created_at: datetime
    updated_at: datetime
    token: Optional[uuid.UUID] = None
