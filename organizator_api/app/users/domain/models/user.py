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


class TShirtSizes(Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"

    @classmethod
    def choices(cls) -> tuple[tuple[str, str], ...]:
        return tuple((i.name, i.value) for i in cls)


class GenderOptions(Enum):
    FEMALE = "Female"
    MALE = "Male"
    NO_BINARY = "No-binary"
    PREFER_NOT_TO_SAY = "Prefer not to say"

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
    date_of_birth: datetime
    study: bool
    work: bool
    university: Optional[str] = None
    degree: Optional[str] = None
    expected_graduation: Optional[datetime] = None
    current_job_role: Optional[str] = None
    tshirt: Optional[TShirtSizes] = None
    gender: Optional[GenderOptions] = None
    alimentary_restrictions: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    devpost: Optional[str] = None
    webpage: Optional[str] = None
    token: Optional[uuid.UUID] = None
