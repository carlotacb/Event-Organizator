import uuid
from datetime import timezone, datetime

from app.events.application.requests import UpdateEventRequest
from app.events.domain.models.event import Event
from app.events.infrastructure.repository_factories import EventRepositoryFactory
from app.users.domain.exceptions import OnlyAuthorizedToOrganizer
from app.users.domain.models.user import UserRoles
from app.users.domain.usecases.get_role_by_token_use_case import GetRoleByTokenUseCase


class UpdateEventUseCase:
    def __init__(self) -> None:
        self.event_repository = EventRepositoryFactory.create()

    def execute(
        self, token: uuid.UUID, event_id: uuid.UUID, event: UpdateEventRequest
    ) -> Event:
        role = GetRoleByTokenUseCase().execute(token=token)

        if role != UserRoles.ORGANIZER and role != UserRoles.ORGANIZER_ADMIN:
            raise OnlyAuthorizedToOrganizer

        original_event = self.event_repository.get(event_id)
        new_event = Event(
            id=event_id,
            name=event.name if event.name else original_event.name,
            description=event.description
            if event.description
            else original_event.description,
            url=event.url if event.url else original_event.url,
            start_date=datetime.strptime(event.start_date, "%d/%m/%Y %H:%M")
            if event.start_date
            else original_event.start_date,
            end_date=datetime.strptime(event.end_date, "%d/%m/%Y %H:%M")
            if event.end_date
            else original_event.end_date,
            location=event.location if event.location else original_event.location,
            header_image=event.header_image
            if event.header_image
            else original_event.header_image,
            created_at=original_event.created_at,
            updated_at=datetime.now(tz=timezone.utc),
            open_for_participants=event.open_for_participants
            if event.open_for_participants is not None
            else original_event.open_for_participants,
            max_participants=event.max_participants
            if event.max_participants
            else original_event.max_participants,
            expected_attrition_rate=event.expected_attrition_rate
            if event.expected_attrition_rate
            else original_event.expected_attrition_rate,
            students_only=event.students_only
            if event.students_only is not None
            else original_event.students_only,
            age_restrictions=event.age_restrictions
            if event.age_restrictions
            else original_event.age_restrictions,
        )

        self.event_repository.update(new_event)

        return new_event
