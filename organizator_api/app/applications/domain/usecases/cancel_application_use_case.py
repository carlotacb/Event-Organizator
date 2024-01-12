import uuid

from app.applications.domain.exceptions import (
    ApplicationCanNotBeCancelled,
    ApplicationIsNotFromUser,
)
from app.applications.domain.models.application import ApplicationStatus
from app.applications.infrastructure.repository_factories import (
    ApplicationRepositoryFactory,
)


class CancelApplicationUseCase:
    def __init__(self) -> None:
        self.application_repository = ApplicationRepositoryFactory.create()

    def execute(self, application_id: uuid.UUID, token: uuid.UUID) -> None:
        application = self.application_repository.get(application_id)

        if application.user.token != token:
            raise ApplicationIsNotFromUser

        if (
            application.status == ApplicationStatus.INVALID
            or application.status == ApplicationStatus.REJECTED
        ):
            raise ApplicationCanNotBeCancelled

        application.status = ApplicationStatus.CANCELLED
        application.updated_at = application.updated_at

        self.application_repository.update(application)
