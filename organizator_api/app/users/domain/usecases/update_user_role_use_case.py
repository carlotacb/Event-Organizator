import uuid
from typing import Optional

from app.users.domain.exceptions import OnlyAuthorizedToOrganizerAdmin
from app.users.domain.models.user import User, UserRoles
from app.users.domain.usecases.get_role_by_token_use_case import GetRoleByTokenUseCase
from app.users.infrastructure.repository_factories import UserRepositoryFactory


class UpdateUserRoleUseCase:
    def __init__(self) -> None:
        self.user_repository = UserRepositoryFactory.create()

    def execute(
        self, token: Optional[uuid.UUID], user_id: uuid.UUID, new_role: str
    ) -> User:
        role = GetRoleByTokenUseCase().execute(token=token)

        if role != UserRoles.ORGANIZER_ADMIN:
            raise OnlyAuthorizedToOrganizerAdmin

        user = self.user_repository.get_by_id(user_id)
        user.role = new_role

        self.user_repository.update(user)
        return user
