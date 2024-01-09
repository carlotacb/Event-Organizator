import uuid
from datetime import datetime, timezone

from app.events.application.requests import CreateEventRequest
from app.events.domain.models.event import Event
from app.events.infrastructure.repository_factories import EventRepositoryFactory
from app.users.domain.exceptions import OnlyAuthorizedToOrganizerAdmin
from app.users.domain.models.user import UserRoles
from app.users.domain.usecases.get_role_by_token_use_case import GetRoleByTokenUseCase


class CreateEventUseCase:
    def __init__(self) -> None:
        self.event_repository = EventRepositoryFactory.create()

    def execute(self, token: uuid.UUID, event_data: CreateEventRequest) -> None:
        role = GetRoleByTokenUseCase().execute(token=token)

        if role != UserRoles.ORGANIZER_ADMIN:
            raise OnlyAuthorizedToOrganizerAdmin

        event = Event(
            id=uuid.uuid4(),
            name=event_data.name,
            url=event_data.url,
            start_date=datetime.strptime(event_data.start_date, "%d/%m/%Y %H:%M"),
            end_date=datetime.strptime(event_data.end_date, "%d/%m/%Y %H:%M"),
            location=event_data.location,
            description=event_data.description,
            header_image=event_data.header_image,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
            open_for_participants=event_data.open_for_participants,
            max_participants=event_data.max_participants,
            expected_attrition_rate=event_data.expected_attrition_rate,
            students_only=event_data.students_only,
            age_restrictions=event_data.age_restrictions,
        )

        self.event_repository.create(event)
