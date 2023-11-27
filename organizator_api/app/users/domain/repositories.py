from abc import ABC, abstractmethod

from app.users.domain.models.user import User


class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> None:
        pass
