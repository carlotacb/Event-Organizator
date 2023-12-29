import uuid

from app.users.domain.models.user import User
from app.users.infrastructure.repository_factories import UserRepositoryFactory


class GetUserByTokenUseCase:
    def __init__(self) -> None:
        self.user_repository = UserRepositoryFactory.create()

    def execute(self, token: uuid.UUID) -> User:
        return self.user_repository.get_by_token(token=token)
