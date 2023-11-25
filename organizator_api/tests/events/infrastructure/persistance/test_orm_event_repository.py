import uuid

from datetime import datetime

from app.events.infrastructure.persistance.models.orm_event import ORMEvent
from app.events.infrastructure.persistance.orm_event_repository import (
    ORMEventRepository,
)
from app.events.domain.exceptions import EventAlreadyExists, EventNotFound
from tests.api_tests import ApiTests
from tests.events.domain.EventFactory import EventFactory


class TestORMEventRepository(ApiTests):
    def test__given_a_event__when_create__then_event_is_saved(self) -> None:
        event = EventFactory().create()

        ORMEventRepository().create(event=event)

        self.assertIsNotNone(ORMEvent.objects.get(id=str(event.id)))

    def test__given_a_event_that_already_exists__when_create__then_raise_exception(
        self,
    ) -> None:
        event = EventFactory().create()
        event2 = EventFactory().create(
            new_id=uuid.UUID("be0f4c18-4a7c-4c1e-8a62-fc50916b6c88")
        )
        ORMEventRepository().create(event=event)

        with self.assertRaises(EventAlreadyExists):
            ORMEventRepository().create(event=event2)

    def test__when_get_all__then_all_events_are_returned(self) -> None:
        event = EventFactory().create()
        event2 = EventFactory().create(
            new_id=uuid.UUID("be0f4c18-4a7c-4c1e-8a62-fc50916b6c88"),
            name="HackUPC 2022",
        )
        ORMEventRepository().create(event=event)
        ORMEventRepository().create(event=event2)

        events = ORMEventRepository().get_all()

        self.assertEqual(len(events), 2)
        self.assertEqual(events[0].id, event.id)
        self.assertEqual(type(events[0].id), uuid.UUID)
        self.assertEqual(events[0].name, event.name)
        self.assertEqual(type(events[0].name), str)
        self.assertEqual(events[0].description, event.description)
        self.assertEqual(type(events[0].description), str)
        self.assertEqual(events[0].url, event.url)
        self.assertEqual(type(events[0].url), str)
        self.assertEqual(type(events[0].start_date), datetime)
        self.assertEqual(type(events[0].end_date), datetime)
        self.assertEqual(type(events[0].location), str)
        self.assertEqual(type(events[0].header_image), str)
        self.assertEqual(type(events[0].created_at), datetime)
        self.assertEqual(type(events[0].updated_at), datetime)
        self.assertEqual(events[1].id, event2.id)
        self.assertEqual(events[1].name, event2.name)
        self.assertEqual(events[1].description, event2.description)
        self.assertEqual(events[1].url, event2.url)

    def test__given_a_event__when_get__then_event_is_returned(self) -> None:
        event = EventFactory().create()
        ORMEventRepository().create(event=event)

        event = ORMEventRepository().get(event_id=event.id)

        self.assertIsNotNone(event)
        self.assertEqual(event.id, event.id)
        self.assertEqual(type(event.id), uuid.UUID)
        self.assertEqual(event.name, event.name)
        self.assertEqual(type(event.name), str)
        self.assertEqual(event.description, event.description)
        self.assertEqual(type(event.description), str)
        self.assertEqual(event.url, event.url)
        self.assertEqual(type(event.url), str)
        self.assertEqual(type(event.start_date), datetime)
        self.assertEqual(type(event.end_date), datetime)
        self.assertEqual(type(event.location), str)
        self.assertEqual(type(event.header_image), str)
        self.assertEqual(type(event.created_at), datetime)
        self.assertEqual(type(event.updated_at), datetime)
        self.assertEqual(event.deleted_at, None)

    def test__when_get_a_non_existing_event__then_raise_event_not_found(self) -> None:
        with self.assertRaises(EventNotFound):
            ORMEventRepository().get(event_id=uuid.uuid4())

    def test__given_a_event__when_update__then_event_is_updated(self) -> None:
        # Given
        event = EventFactory().create(name="HackUPC 2021")
        ORMEventRepository().create(event=event)

        # When
        event.name = "HackUPC 2022"
        ORMEventRepository().update(event=event)
        event = ORMEventRepository().get(event_id=event.id)

        # Then
        self.assertEqual(event.name, "HackUPC 2022")
        self.assertEqual(type(event.name), str)

    def test__given_a_event__when_update_with_a_name_that_already_exists__then_it_raises_event_already_exists(
        self,
    ) -> None:
        # Given
        event = EventFactory().create(name="HackUPC 2021")
        event2 = EventFactory().create(
            new_id=uuid.UUID("be0f4c18-4a7c-4c1e-8a62-fc50916b6c88"),
            name="HackUPC 2022",
        )
        ORMEventRepository().create(event=event)
        ORMEventRepository().create(event=event2)

        # When
        event.name = "HackUPC 2022"

        # Then
        with self.assertRaises(EventAlreadyExists):
            ORMEventRepository().update(event=event)

    def test__given_no_events_when_update_a_non_existing_event__then_it_raises_event_not_found(
        self,
    ) -> None:
        # Given
        event = EventFactory().create(name="HackUPC 2021")

        # When
        event.name = "HackUPC 2022"

        # Then
        with self.assertRaises(EventNotFound):
            ORMEventRepository().update(event=event)