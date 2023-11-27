import uuid

from app.users.infrastructure.repository_factories import UserRepositoryFactory
from app.users.domain.models.user import User


class GetByIdUseCase:
    def __init__(self) -> None:
        self.user_repository = UserRepositoryFactory.create()

    def execute(self, user_id: uuid.UUID) -> User:
        return self.user_repository.get_by_id(user_id=user_id)
