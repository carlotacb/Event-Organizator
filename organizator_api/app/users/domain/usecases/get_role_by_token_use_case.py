import uuid
from typing import Optional

from app.users.domain.models.user import User, UserRoles
from app.users.infrastructure.repository_factories import UserRepositoryFactory


class GetRoleByTokenUseCase:
    def __init__(self) -> None:
        self.user_repository = UserRepositoryFactory.create()

    def execute(self, token: Optional[uuid.UUID]) -> UserRoles:
        user = self.user_repository.get_by_token(token=token)
        return user.role
