from app.events.infrastructure.persistance.models.orm_event import ORMEvent
from app.events.infrastructure.persistance.orm_event_repository import ORMEventRepository
from tests.api_tests import ApiTests
from tests.events.domain.EventFactory import EventFactory


class TestORMEventRepository(ApiTests):
    def test__given_a_event__when_create__then_event_is_saved(self) -> None:
        event = EventFactory().create()

        ORMEventRepository().create(event=event)

        self.assertIsNotNone(ORMEvent.objects.get(id=str(event.id)))