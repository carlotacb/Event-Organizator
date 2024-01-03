import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class UserRoles(Enum):
    PARTICIPANT = "Participant"
    ORGANIZER = "Organizer"
    ORGANIZER_ADMIN = "Organizer admin"

    @classmethod
    def choices(cls) -> tuple[tuple[str, str], ...]:
        return tuple((i.name, i.value) for i in cls)


@dataclass
class User:
    id: uuid.UUID
    email: str
    password: bytes
    first_name: str
    last_name: str
    username: str
    bio: str
    profile_image: str
    role: UserRoles
    created_at: datetime
    updated_at: datetime
    token: Optional[uuid.UUID] = None
