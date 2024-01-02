import json
import uuid
from datetime import datetime

from tests.api_tests import ApiTests
from tests.events.domain.EventFactory import EventFactory


class TestEventViews(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.event_repository.clear()
        self.request_body = {
            "name": "HackNight Ep.VI",
            "url": "https://www.hacknights.dev",
            "description": "The best hack-night ever",
            "start_date": "17/11/2023 21:00",
            "end_date": "18/11/2023 05:00",
            "location": "Aula d'estudis Campus Nord",
            "header_image": "https://www.hacknights.dev/images/hacknight.png",
        }

    def test__given_unexpected_body__when_create_event__then_bad_request_is_returned(
        self,
    ) -> None:
        # Given
        body = {}  # type: ignore

        # When
        response = self.client.post(
            "/organizator-api/events/new",
            json.dumps(body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Unexpected body")

    def test__given_a_event_with_the_same_name_as_one_already_created__when_create_event__then_returns_409(
        self,
    ) -> None:
        # When
        self.client.post(
            "/organizator-api/events/new",
            json.dumps(self.request_body),
            content_type="application/json",
        )
        response = self.client.post(
            "/organizator-api/events/new",
            json.dumps(self.request_body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.content, b"Event already exists")

    def test__given_a_json_body_with_an_event__when_creat_event__then_the_event_is_created_and_stored_in_db(
        self,
    ) -> None:
        # When
        response = self.client.post(
            "/organizator-api/events/new",
            json.dumps(self.request_body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content, b"Event created correctly")

        events = self.event_repository.get_all()
        self.assertEqual(len(events), 1)
        event = events.pop()
        self.assertEqual(event.name, "HackNight Ep.VI")
        self.assertEqual(event.url, "https://www.hacknights.dev")
        self.assertEqual(event.description, "The best hack-night ever")
        self.assertEqual(event.start_date, datetime(2023, 11, 17, 21, 0))
        self.assertEqual(event.end_date, datetime(2023, 11, 18, 5, 0))
        self.assertEqual(event.location, "Aula d'estudis Campus Nord")
        self.assertEqual(
            event.header_image, "https://www.hacknights.dev/images/hacknight.png"
        )

    def test__given_no_events_in_db__when_get_all_events__then_returns_empty_list(
        self,
    ) -> None:
        # When
        response = self.client.get("/organizator-api/events/")

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"[]")

    def test__given_events_in_db__when_get_all_events__then_returns_the_events_list(
        self,
    ) -> None:
        # Given
        event = EventFactory().create()
        event2 = EventFactory().create(
            new_id=uuid.UUID("be0f4c18-4a7c-4c1e-8a62-fc50916b6c88"),
            name="HackUPC 2022",
        )
        self.event_repository.create(event)
        self.event_repository.create(event2)

        # When
        response = self.client.get("/organizator-api/events/")

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'[{"id": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc", "name": "HackUPC 2023", "url": "https://www.hackupc.com/", "description": "The biggest student hackathon in Europe", "start_date": "2023-05-12T16:00:00Z", "end_date": "2023-05-14T18:00:00Z", "location": "UPC Campus Nord", "header_image": "https://hackupc.com/ogimage.png", "deleted": false}, {"id": "be0f4c18-4a7c-4c1e-8a62-fc50916b6c88", "name": "HackUPC 2022", "url": "https://www.hackupc.com/", "description": "The biggest student hackathon in Europe", "start_date": "2023-05-12T16:00:00Z", "end_date": "2023-05-14T18:00:00Z", "location": "UPC Campus Nord", "header_image": "https://hackupc.com/ogimage.png", "deleted": false}]',
        )

    def test__given_events_in_db__when_get_all_upcoming_events__then_returns_the_events_list(
        self,
    ) -> None:
        # Given
        event = EventFactory().create()
        event2 = EventFactory().create(
            new_id=uuid.UUID("be0f4c18-4a7c-4c1e-8a62-fc50916b6c88"),
            name="HackUPC 2025",
            start_date=datetime(2025, 5, 12, 16, 0),
            end_date=datetime(2025, 5, 14, 18, 0),
        )
        self.event_repository.create(event)
        self.event_repository.create(event2)

        # When
        response = self.client.get("/organizator-api/events/upcoming")

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'[{"id": "be0f4c18-4a7c-4c1e-8a62-fc50916b6c88", "name": "HackUPC 2025", "url": "https://www.hackupc.com/", "description": "The biggest student hackathon in Europe", "start_date": "2025-05-12T16:00:00Z", "end_date": "2025-05-14T18:00:00Z", "location": "UPC Campus Nord", "header_image": "https://hackupc.com/ogimage.png", "deleted": false}]',
        )

    def test__given_events_in_db__when_get_event_by_id__then_returns_the_event(
        self,
    ) -> None:
        # Given
        event = EventFactory().create()
        self.event_repository.create(event)

        # When
        response = self.client.get(
            "/organizator-api/events/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"id": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc", "name": "HackUPC 2023", "url": "https://www.hackupc.com/", "description": "The biggest student hackathon in Europe", "start_date": "2023-05-12T16:00:00Z", "end_date": "2023-05-14T18:00:00Z", "location": "UPC Campus Nord", "header_image": "https://hackupc.com/ogimage.png", "deleted": false}',
        )

    def test__when_get_event_by_nonexistent_id__then_returns_the_event(
        self,
    ) -> None:
        # When
        response = self.client.get(
            "/organizator-api/events/ef6f6fb3-ba12-43dd-a0da-95de8125b1c4"
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.content,
            b"Event does not exist",
        )

    def test__given_information_to_update_an_event__when_update_event__then_the_event_is_updated(
        self,
    ) -> None:
        # Given
        event = EventFactory().create()
        self.event_repository.create(event)
        request_body = {
            "name": "HackNight Ep.VI",
            "url": "https://www.hacknights.dev",
            "description": "The best hack-night ever",
            "start_date": "2023-11-17T21:00:00Z",
            "end_date": "2023-11-18T05:00:00Z",
            "location": "Aula d'estudis Campus Nord",
            "header_image": "https://www.hacknights.dev/images/hacknight.png",
        }

        # When
        response = self.client.post(
            "/organizator-api/events/update/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
            json.dumps(request_body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"id": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc", "name": "HackNight Ep.VI", "url": "https://www.hacknights.dev", "description": "The best hack-night ever", "start_date": "2023-11-17T21:00:00Z", "end_date": "2023-11-18T05:00:00Z", "location": "Aula d\'estudis Campus Nord", "header_image": "https://www.hacknights.dev/images/hacknight.png", "deleted": false}',
        )

        events = self.event_repository.get_all()
        self.assertEqual(len(events), 1)
        event = events.pop()
        self.assertEqual(event.name, "HackNight Ep.VI")
        self.assertEqual(event.url, "https://www.hacknights.dev")
        self.assertEqual(event.description, "The best hack-night ever")
        self.assertEqual(event.start_date, datetime(2023, 11, 17, 21, 0))
        self.assertEqual(event.end_date, datetime(2023, 11, 18, 5, 0))
        self.assertEqual(event.location, "Aula d'estudis Campus Nord")
        self.assertEqual(
            event.header_image, "https://www.hacknights.dev/images/hacknight.png"
        )

    def test__given_only_some_information_to_update_an_event__when_update_event__then_the_event_is_updated(
        self,
    ) -> None:
        # Given
        event = EventFactory().create()
        self.event_repository.create(event)
        request_body = {
            "description": "The biggest student hackathon in Europe taking place in Barcelona",
            "url": "https://2023.hackupc.com/",
        }

        # When
        response = self.client.post(
            "/organizator-api/events/update/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
            json.dumps(request_body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"id": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc", "name": "HackUPC 2023", "url": "https://2023.hackupc.com/", "description": "The biggest student hackathon in Europe taking place in Barcelona", "start_date": "2023-05-12T16:00:00Z", "end_date": "2023-05-14T18:00:00Z", "location": "UPC Campus Nord", "header_image": "https://hackupc.com/ogimage.png", "deleted": false}',
        )

        events = self.event_repository.get_all()
        self.assertEqual(len(events), 1)
        event = events.pop()
        self.assertEqual(event.url, "https://2023.hackupc.com/")
        self.assertEqual(
            event.description,
            "The biggest student hackathon in Europe taking place in Barcelona",
        )

    def test__given_a_event_with_the_same_name_as_one_already_created__when_update_event__then_returns_409(
        self,
    ) -> None:
        # Given
        event = EventFactory().create()
        event2 = EventFactory().create(
            new_id=uuid.UUID("be0f4c18-4a7c-4c1e-8a62-fc50916b6c88"),
            name="HackUPC 2022",
        )
        self.event_repository.create(event)
        self.event_repository.create(event2)

        request_body = {"name": "HackUPC 2022"}

        # When
        response = self.client.post(
            "/organizator-api/events/update/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
            json.dumps(request_body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.content, b"Event already exists")

    def test__given_no_event_in_db__when_update_event__then_returns_404(
        self,
    ) -> None:
        # Given
        request_body = {"name": "HackUPC 2022"}

        # When
        response = self.client.post(
            "/organizator-api/events/update/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
            json.dumps(request_body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"Event does not exist")

    def test__given_a_event__when_delete_event__then_the_event_is_deleted(
        self,
    ) -> None:
        # Given
        event = EventFactory().create()
        self.event_repository.create(event)

        # When
        response = self.client.post(
            "/organizator-api/events/delete/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Event updated correctly to be deleted")

    def test__given_no_event_in_db__when_delete_event__then_returns_404(
        self,
    ) -> None:
        # When
        response = self.client.post(
            "/organizator-api/events/delete/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"Event does not exist")
