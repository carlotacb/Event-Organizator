from django.db import IntegrityError

from app.users.domain.models.user import User
from app.users.domain.repositories import UserRepository
from app.users.domain.exceptions import UserAlreadyExists
from app.users.infrastructure.persistance.models.orm_user import ORMUser


class ORMUserRepository(UserRepository):
    def create(self, user: User) -> None:
        try:
            self._to_model(user).save()
        except IntegrityError:
            raise UserAlreadyExists()

    def _to_model(self, user: User) -> ORMUser:
        return ORMUser(
            id=user.id,
            email=user.email,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            bio=user.bio,
            profile_image=user.profile_image,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
