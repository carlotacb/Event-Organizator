from dataclasses import dataclass
from typing import Optional

@dataclass
class CreateUserRequest:
    email: str
    password: str
    first_name: str
    last_name: str
    username: str
    bio: str
    profile_image: str
    date_of_birth: str
    study: bool
    work: bool
    university: Optional[str] = None
    degree: Optional[str] = None
    expected_graduation: Optional[str] = None
    current_job_role: Optional[str] = None


@dataclass
class UpdateUserRequest:
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
