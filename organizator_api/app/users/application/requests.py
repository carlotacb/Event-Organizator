from dataclasses import dataclass


@dataclass
class CreateUserRequest:
    email: str
    password: str
    first_name: str
    last_name: str
    username: str
    bio: str
    profile_image: str