from abc import ABC, abstractmethod
from typing import List

from app.users.domain.models.user import User


class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[User]:
        pass