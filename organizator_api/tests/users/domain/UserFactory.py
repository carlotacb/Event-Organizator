import uuid
from datetime import datetime

from app.users.domain.models.user import User


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
        profile_image: str = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png",
        token: uuid.UUID = None,
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
    ) -> User:
        return User(
            id=new_id,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            username=username,
            bio=bio,
            profile_image=profile_image,
            token=token,
            created_at=created_at,
            updated_at=updated_at,
        )
