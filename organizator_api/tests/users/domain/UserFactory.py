import uuid
import bcrypt
from datetime import datetime, date
from typing import Optional

from app.users.domain.models.user import User, UserRoles, GenderOptions, TShirtSizes


class UserFactory:
    @staticmethod
    def create(
        new_id: uuid.UUID = uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"),
        email: str = "carlota@hackupc.com",
        password: str = "123456",
        first_name: str = "Carlota",
        last_name: str = "Catot",
        username: str = "carlotacb",
        bio: str = "The user that is using this application",
        profile_image: str = "profile_picture.png",
        token: Optional[uuid.UUID] = None,
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
        role: UserRoles = UserRoles.PARTICIPANT,
        date_of_birth: datetime = datetime(1996, 5, 7),
        study: bool = True,
        work: bool = False,
        university: Optional[str] = "Universitat Politècnica de Catalunya",
        degree: Optional[str] = "Computer Science",
        expected_graduation: Optional[datetime] = datetime(2024, 5, 1),
        current_job_role: Optional[str] = None,
        tshirt: Optional[TShirtSizes] = None,
        gender: Optional[GenderOptions] = None,
        alimentary_restrictions: Optional[str] = None,
        github: Optional[str] = None,
        linkedin: Optional[str] = None,
        devpost: Optional[str] = None,
        webpage: Optional[str] = None,
    ) -> User:
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        return User(
            id=new_id,
            email=email,
            password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            username=username,
            bio=bio,
            profile_image=profile_image,
            token=token,
            created_at=created_at,
            updated_at=updated_at,
            role=role,
            date_of_birth=date_of_birth,
            study=study,
            work=work,
            university=university,
            degree=degree,
            expected_graduation=expected_graduation,
            current_job_role=current_job_role,
            tshirt=tshirt,
            gender=gender,
            alimentary_restrictions=alimentary_restrictions,
            github=github,
            linkedin=linkedin,
            devpost=devpost,
            webpage=webpage,
        )
