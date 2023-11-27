from app.events.domain.repositories import EventRepository
from app.events.infrastructure.persistence.orm_event_repository import (
    ORMEventRepository,
)


class EventRepositoryFactory:
    _events_repository = None

    @staticmethod
    def create() -> EventRepository:
        if EventRepositoryFactory._events_repository is None:
            EventRepositoryFactory._events_repository = ORMEventRepository()

        return EventRepositoryFactory._events_repository
