import uuid
from datetime import datetime, timezone

from app.events.infrastructure.repository_factories import EventRepositoryFactory
from app.users.domain.exceptions import OnlyAuthorizedToOrganizerAdmin
from app.users.domain.models.user import UserRoles
from app.users.domain.usecases.get_role_by_token_use_case import GetRoleByTokenUseCase


class DeleteEventUseCase:
    def __init__(self) -> None:
        self.event_repository = EventRepositoryFactory.create()

    def execute(self, token: uuid.UUID, event_id: uuid.UUID) -> None:
        role = GetRoleByTokenUseCase().execute(token=token)

        if role != UserRoles.ORGANIZER_ADMIN:
            raise OnlyAuthorizedToOrganizerAdmin

        self.event_repository.delete(
            event_id=event_id, delete_time=datetime.now(timezone.utc)
        )
