from typing import List

from app.users.domain.repositories import UserRepository
from app.users.domain.models.user import User
from app.users.domain.exceptions import UserAlreadyExists


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

    def clear(self) -> None:
        self.users = []
