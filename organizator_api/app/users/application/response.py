from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from app.users.domain.models.user import User, UserRoles, GenderOptions


@dataclass
class UserResponse:
    id: str
    username: str
    email: str
    first_name: str
    last_name: str
    bio: str
    profile_image: str
    role: UserRoles
    date_of_birth: datetime
    study: bool
    work: bool
    university: str
    degree: str
    current_job_role: str
    tshirt: str
    gender: str
    alimentary_restrictions: str
    github: str
    linkedin: str
    devpost: str
    webpage: str
    expected_graduation: Optional[datetime] = None

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
            role=user.role,
            date_of_birth=user.date_of_birth,
            study=user.study,
            work=user.work,
            university=user.university if user.university else "",
            degree=user.degree if user.degree else "",
            expected_graduation=user.expected_graduation if user.expected_graduation else None,
            current_job_role=user.current_job_role if user.current_job_role else "",
            tshirt=user.tshirt.value if user.tshirt else "",
            gender=user.gender.value if user.gender else "",
            alimentary_restrictions=user.alimentary_restrictions if user.alimentary_restrictions else "",
            github=user.github if user.github else "",
            linkedin=user.linkedin if user.linkedin else "",
            devpost=user.devpost if user.devpost else "",
            webpage=user.webpage if user.webpage else "",
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
            "role": self.role.value,
            "date_of_birth": self.date_of_birth.strftime("%d/%m/%Y"),
            "study": self.study,
            "work": self.work,
            "university": self.university,
            "degree": self.degree,
            "expected_graduation": self.expected_graduation.strftime("%d/%m/%Y") if self.expected_graduation else None,
            "current_job_role": self.current_job_role,
            "tshirt": self.tshirt,
            "gender": self.gender,
            "alimentary_restrictions": self.alimentary_restrictions,
            "github": self.github,
            "linkedin": self.linkedin,
            "devpost": self.devpost,
            "webpage": self.webpage,
        }
