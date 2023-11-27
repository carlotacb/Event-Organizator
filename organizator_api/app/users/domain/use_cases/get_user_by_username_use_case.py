from app.users.infrastructure.repository_factories import UserRepositoryFactory
from app.users.domain.models.user import User


class GetUserByUsernameUseCase:
    def __init__(self) -> None:
        self.user_repository = UserRepositoryFactory.create()

    def execute(self, username: str) -> User:
        return self.user_repository.get_by_username(username=username)