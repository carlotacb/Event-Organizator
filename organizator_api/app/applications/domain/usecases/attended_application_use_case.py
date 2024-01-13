import uuid

from app.applications.domain.exceptions import ApplicationCanNotBeAttended
from app.applications.domain.models.application import ApplicationStatus
from app.applications.infrastructure.repository_factories import (
    ApplicationRepositoryFactory,
)
from app.users.domain.exceptions import OnlyAuthorizedToOrganizer
from app.users.domain.models.user import UserRoles
from app.users.domain.usecases.get_role_by_token_use_case import GetRoleByTokenUseCase


class AttendedApplicationUseCase:
    def __init__(self) -> None:
        self.application_repository = ApplicationRepositoryFactory.create()

    def execute(self, application_id: uuid.UUID, token: uuid.UUID) -> None:
        role = GetRoleByTokenUseCase().execute(token=token)

        if role != UserRoles.ORGANIZER and role != UserRoles.ORGANIZER_ADMIN:
            raise OnlyAuthorizedToOrganizer

        application = self.application_repository.get(application_id)

        if application.status != ApplicationStatus.CONFIRMED:
            raise ApplicationCanNotBeAttended

        application.status = ApplicationStatus.ATTENDED
        application.updated_at = application.updated_at

        self.application_repository.update(application)
