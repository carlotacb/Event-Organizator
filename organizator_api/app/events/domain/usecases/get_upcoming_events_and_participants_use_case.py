import uuid
from datetime import datetime
from typing import List

from app.applications.domain.usecases.get_applications_by_event_use_case import (
    GetApplicationsByEventUseCase,
)
from app.events.domain.models.event_applications import EventApplication
from app.events.infrastructure.repository_factories import EventRepositoryFactory
from app.users.domain.exceptions import OnlyAuthorizedToOrganizer
from app.users.domain.models.user import UserRoles
from app.users.domain.usecases.get_role_by_token_use_case import GetRoleByTokenUseCase


class GetUpcomingEventsAndParticipantsUseCase:
    def __init__(self) -> None:
        self.event_repository = EventRepositoryFactory.create()

    def execute(self, token: uuid.UUID) -> List[EventApplication]:
        role = GetRoleByTokenUseCase().execute(token=token)

        if role != UserRoles.ORGANIZER_ADMIN and role != UserRoles.ORGANIZER:
            raise OnlyAuthorizedToOrganizer

        response = []
        events = self.event_repository.get_all()

        for event in events:
            if event.deleted_at is None and event.start_date > datetime.now(
                tz=event.start_date.tzinfo
            ):
                participants = GetApplicationsByEventUseCase().execute(
                    event_id=event.id, token=token
                )

                response.append(
                    EventApplication(
                        event_id=event.id,
                        name=event.name,
                        actual_participants_count=len(participants),
                        max_participants=event.max_participants,
                        expected_attrition_rate=event.expected_attrition_rate,
                    )
                )

        return response
