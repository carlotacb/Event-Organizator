from typing import List

from app.users.domain.models.user import User
from app.users.infrastructure.repository_factories import UserRepositoryFactory


class GetAllUsersUseCase:
    def __init__(self) -> None:
        self.user_repository = UserRepositoryFactory.create()

    def execute(self) -> List[User]:
        return self.user_repository.get_all()
