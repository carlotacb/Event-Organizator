from typing import List

from app.events.domain.models.event import Event
from app.events.infrastructure.repository_factories import EventRepositoryFactory


class GetAllEventsUseCase:
    def __init__(self) -> None:
        self.event_repository = EventRepositoryFactory.create()

    def execute(self) -> List[Event]:
        return self.event_repository.get_all()
