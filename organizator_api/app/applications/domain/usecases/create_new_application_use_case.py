import uuid
from datetime import datetime, timezone, date

from app.applications.domain.exceptions import (
    ProfileNotComplete,
    UserIsNotAParticipant,
    UserIsNotStudent,
    UserIsTooYoung, EventAlreadyStarted,
)
from app.applications.domain.models.application import Application, ApplicationStatus
from app.applications.infrastructure.repository_factories import (
    ApplicationRepositoryFactory,
)
from app.events.domain.usecases.get_event_use_case import GetEventUseCase
from app.users.domain.models.user import UserRoles
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

        if user.role != UserRoles.PARTICIPANT:
            raise UserIsNotAParticipant

        event = GetEventUseCase().execute(event_id=event_id)

        if event.students_only and not user.study:
            raise UserIsNotStudent

        today = date.today()
        age = (
            today.year
            - user.date_of_birth.year
            - (
                (today.month, today.day)
                < (user.date_of_birth.month, user.date_of_birth.day)
            )
        )

        if age < event.age_restrictions:
            raise UserIsTooYoung

        if event.start_date < datetime.now():
            raise EventAlreadyStarted

        application = Application(
            id=uuid.uuid4(),
            user=user,
            event=event,
            status=ApplicationStatus.PENDING,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        )

        self.application_repository.create(application)
