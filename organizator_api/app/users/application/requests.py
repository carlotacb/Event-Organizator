from dataclasses import dataclass
from typing import Optional

from app.users.domain.models.user import UserRoles


@dataclass
class CreateUserRequest:
    email: str
    password: str
    first_name: str
    last_name: str
    username: str
    bio: str
    profile_image: str
    role: Optional[str] = UserRoles.PARTICIPANT.name


@dataclass
class UpdateUserRequest:
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    role: Optional[str] = None
