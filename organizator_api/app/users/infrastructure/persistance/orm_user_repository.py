import uuid

from django.db import IntegrityError
from typing import List

from app.users.domain.models.user import User
from app.users.domain.repositories import UserRepository
from app.users.domain.exceptions import UserAlreadyExists, UserNotFound
from app.users.infrastructure.persistance.models.orm_user import ORMUser


class ORMUserRepository(UserRepository):
    def create(self, user: User) -> None:
        try:
            self._to_model(user).save()
        except IntegrityError:
            raise UserAlreadyExists()

    def get_all(self) -> List[User]:
        return [self._to_domain(user) for user in ORMUser.objects.all()]

    def get_by_id(self, user_id: uuid.UUID) -> User:
        try:
            user = self._to_domain(ORMUser.objects.get(id=user_id))
            return user
        except ORMUser.DoesNotExist:
            raise UserNotFound()

    def get_by_username(self, username: str) -> User:
        try:
            user = self._to_domain(ORMUser.objects.get(username=username))
            return user
        except ORMUser.DoesNotExist:
            raise UserNotFound()

    def update(self, user: User) -> None:
        try:
            orm_user = ORMUser.objects.get(id=user.id)
            orm_user.first_name = user.first_name
            orm_user.last_name = user.last_name
            orm_user.username = user.username
            orm_user.bio = user.bio
            orm_user.profile_image = user.profile_image
            orm_user.updated_at = user.updated_at
            orm_user.save()
        except ORMUser.DoesNotExist:
            raise UserNotFound()
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

    def _to_domain(self, user: ORMUser) -> User:
        return User(
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
