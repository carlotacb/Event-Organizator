import uuid
from datetime import datetime, timezone

from app.applications.domain.exceptions import ProfileNotComplete
from app.applications.domain.models.application import Application
from app.applications.infrastructure.repository_factories import (
    ApplicationRepositoryFactory,
)
from app.events.domain.usecases.get_event_use_case import GetEventUseCase
from app.users.domain.usecases.get_user_by_token_use_case import GetUserByTokenUseCase


class CreateNewApplicationUseCase:
    def __init__(self) -> None:
        self.application_repository = ApplicationRepositoryFactory.create()

    def execute(self, token: uuid.UUID, event_id: uuid.UUID) -> None:
        user = GetUserByTokenUseCase().execute(token=token)
        if (
            user.gender is None
            or user.tshirt is None
            or user.alimentary_restrictions is None
        ):
            raise ProfileNotComplete

        event = GetEventUseCase().execute(event_id=event_id)

        application = Application(
            id=uuid.uuid4(),
            user=user,
            event=event,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        )

        self.application_repository.create(application)
