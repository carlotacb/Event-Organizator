from dataclasses import dataclass
from typing import Any

from app.users.domain.models.user import User


@dataclass
class UserResponse:
    id: str
    username: str
    email: str
    first_name: str
    last_name: str
    bio: str
    profile_image: str

    @staticmethod
    def from_user(user: User) -> "UserResponse":
        return UserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            bio=user.bio,
            profile_image=user.profile_image,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "bio": self.bio,
            "profile_image": self.profile_image,
        }
