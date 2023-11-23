from typing import List

from app.events.infrastructure.repository_factories import EventRepositoryFactory
from app.events.domain.models.event import Event


class GetAllEventsUseCase:
    def __init__(self):
        self.event_repository = EventRepositoryFactory.create()

    def execute(self) -> List[Event]:
        return self.event_repository.get_all()
