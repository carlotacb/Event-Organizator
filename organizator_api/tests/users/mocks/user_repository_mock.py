import uuid
from typing import List

from app.users.domain.exceptions import UserAlreadyExists, UserNotFound
from app.users.domain.models.user import User
from app.users.domain.repositories import UserRepository


class UserRepositoryMock(UserRepository):
    def __init__(self) -> None:
        self.users: List[User] = []

    def create(self, user: User) -> None:
        for u in self.users:
            if user.username == u.username:
                raise UserAlreadyExists()
        self.users.append(user)

    def get_all(self) -> List[User]:
        return self.users

    def get_by_id(self, user_id: uuid.UUID) -> User:
        for user in self.users:
            if user.id == user_id:
                return user
        raise UserNotFound()

    def get_by_token(self, token: uuid.UUID) -> User:
        for user in self.users:
            if user.token == token:
                return user
        raise UserNotFound()

    def get_by_username(self, username: str) -> User:
        for user in self.users:
            if user.username == username:
                return user
        raise UserNotFound()

    def update(self, user: User) -> None:
        for u in self.users:
            if (
                u.username == user.username or u.email == user.email
            ) and user.id != u.id:
                raise UserAlreadyExists()
        for u in self.users:
            if user.id == u.id:
                u.first_name = user.first_name
                u.last_name = user.last_name
                u.username = user.username
                u.bio = user.bio
                u.profile_image = user.profile_image
                u.updated_at = user.updated_at
                return
        raise UserNotFound()

    def clear(self) -> None:
        self.users = []
