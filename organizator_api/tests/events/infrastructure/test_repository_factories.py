from django.test import TestCase

from app.events.domain.repositories import EventRepository
from app.events.infrastructure.repository_factories import EventRepositoryFactory


class TestRepositoryFactories(TestCase):
    def test__given_event_repository_factory__when_create__then_returns_event_repository(self) -> None:
        repository = EventRepositoryFactory.create()
        assert isinstance(repository, EventRepository)