import uuid

from app.applications.domain.exceptions import (
    ApplicationNotFound,
    NotApplied,
    UserIsNotAParticipant,
)
from app.applications.domain.models.application import ApplicationStatus
from app.applications.infrastructure.repository_factories import (
    ApplicationRepositoryFactory,
)
from app.events.domain.usecases.get_event_use_case import GetEventUseCase
from app.users.domain.models.user import UserRoles
from app.users.domain.usecases.get_user_by_token_use_case import GetUserByTokenUseCase


class GetApplicationStatusByEventUseCase:
    def __init__(self) -> None:
        self.application_repository = ApplicationRepositoryFactory.create()

    def execute(self, token: uuid.UUID, event_id: uuid.UUID) -> ApplicationStatus:
        GetEventUseCase().execute(event_id=event_id)
        user = GetUserByTokenUseCase().execute(token=token)

        try:
            application = self.application_repository.get_application(
                event_id=event_id, user_id=user.id
            )
        except ApplicationNotFound:
            if user.role == UserRoles.PARTICIPANT:
                raise NotApplied
            else:
                raise UserIsNotAParticipant

        return application.status
