from typing import List

from app.users.infrastructure.repository_factories import UserRepositoryFactory
from app.users.domain.models.user import User


class GetAllUsersUseCase:
    def __init__(self) -> None:
        self.user_repository = UserRepositoryFactory.create()

    def execute(self) -> List[User]:
        return self.user_repository.get_all()
