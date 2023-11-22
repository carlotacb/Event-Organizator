import json
from datetime import datetime

from tests.api_tests import ApiTests


class TestEventViews(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.event_repository.clear()
        self.request_body = {
            "name": "HackNight Ep.VI",
            "url": "https://www.hacknights.dev",
            "description": "The best hack-night ever",
            "start_date": "2023-11-17T21:00:00Z",
            "end_date": "2023-11-18T05:00:00Z",
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

    def test__given_a_event_with_the_same_name_as_one_already_created__when_create_event__then_returns_409(self) -> None:
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
