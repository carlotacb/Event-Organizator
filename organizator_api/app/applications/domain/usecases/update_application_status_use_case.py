import uuid
from datetime import timezone, datetime

from app.applications.domain.exceptions import StatusNotFound
from app.applications.domain.models.application import ApplicationStatus
from app.applications.infrastructure.repository_factories import (
    ApplicationRepositoryFactory,
)
from app.users.domain.exceptions import OnlyAuthorizedToOrganizerAdmin
from app.users.domain.models.user import UserRoles
from app.users.domain.usecases.get_role_by_token_use_case import GetRoleByTokenUseCase


class UpdateApplicationStatusUseCase:
    def __init__(self) -> None:
        self.application_repository = ApplicationRepositoryFactory.create()

    def execute(
        self, application_id: uuid.UUID, status: ApplicationStatus, token: uuid.UUID
    ) -> None:
        role = GetRoleByTokenUseCase().execute(token=token)

        if role != UserRoles.ORGANIZER_ADMIN:
            raise OnlyAuthorizedToOrganizerAdmin

        application = self.application_repository.get(application_id)

        application.status = status
        application.updated_at = datetime.now(tz=timezone.utc)

        self.application_repository.update(application)
