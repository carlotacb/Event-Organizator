import uuid
from typing import List

from app.applications.domain.models.application import Application
from app.applications.infrastructure.repository_factories import (
    ApplicationRepositoryFactory,
)
from app.events.domain.usecases.get_event_use_case import GetEventUseCase
from app.users.domain.exceptions import OnlyAuthorizedToOrganizer
from app.users.domain.models.user import UserRoles
from app.users.domain.usecases.get_role_by_token_use_case import GetRoleByTokenUseCase


class GetApplicationsByEventUseCase:
    def __init__(self) -> None:
        self.application_repository = ApplicationRepositoryFactory.create()

    def execute(self, token: uuid.UUID, event_id: uuid.UUID) -> List[Application]:
        role = GetRoleByTokenUseCase().execute(token=token)

        if role != UserRoles.ORGANIZER_ADMIN and role != UserRoles.ORGANIZER:
            raise OnlyAuthorizedToOrganizer

        event = GetEventUseCase().execute(event_id=event_id)

        return self.application_repository.get_by_event(event_id=event.id)
