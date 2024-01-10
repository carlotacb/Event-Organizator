import json
import uuid
from datetime import datetime

from app.users.domain.models.user import UserRoles
from tests.api_tests import ApiTests
from tests.applications.domain.ApplicationFactory import ApplicationFactory
from tests.events.domain.EventFactory import EventFactory
from tests.users.domain.UserFactory import UserFactory


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
            "open_for_participants": True,
            "max_participants": 100,
            "expected_attrition_rate": 0.1,
            "students_only": True,
            "age_restrictions": 16,
        }
        self.user_repository.clear()
        self.user_admin_token = uuid.UUID("5b90906e-2894-467d-835e-3e4fbe42af9f")
        user_admin = UserFactory().create(
            token=self.user_admin_token, role=UserRoles.ORGANIZER_ADMIN
        )
        self.user_repository.create(user_admin)

        self.user_participant_token = uuid.UUID("ebd8a0f2-eeba-4ddc-b4b9-ab5592ad8e75")
        self.user_participant = UserFactory().create(
            token=self.user_participant_token,
            role=UserRoles.PARTICIPANT,
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            username="user_participant",
            email="user@participant.com",
        )
        self.user_repository.create(self.user_participant)

    def test__given_unexpected_body__when_create_event__then_bad_request_is_returned(
        self,
    ) -> None:
        # Given
        body = {}  # type: ignore

        # When
        header = {"HTTP_AUTHORIZATION": f"{self.user_admin_token}"}
        response = self.client.post(
            "/organizator-api/events/new",
            json.dumps(body),
            content_type="application/json",
            **header,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Unexpected body")

    def test__given_a_event_with_the_same_name_as_one_already_created_created_by_a_admin_user__when_create_event__then_returns_409(
        self,
    ) -> None:
        # When
        header = {"HTTP_AUTHORIZATION": f"{self.user_admin_token}"}
        self.client.post(
            "/organizator-api/events/new",
            json.dumps(self.request_body),
            content_type="application/json",
            **header,  # type: ignore
        )
        response = self.client.post(
            "/organizator-api/events/new",
            json.dumps(self.request_body),
            content_type="application/json",
            **header,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.content, b"Event already exists")

    def test__given_a_json_body_with_an_event__when_creat_event__then_the_event_is_created_and_stored_in_db(
        self,
    ) -> None:
        # When
        header = {"HTTP_AUTHORIZATION": f"{self.user_admin_token}"}
        response = self.client.post(
            "/organizator-api/events/new",
            json.dumps(self.request_body),
            content_type="application/json",
            **header,  # type: ignore
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

    def test__given_a_json_body_with_an_event__when_create_event_without_header__then_it_returns_401(
        self,
    ) -> None:
        # When
        response = self.client.post(
            "/organizator-api/events/new",
            json.dumps(self.request_body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"Unauthorized")

    def test__given_a_json_body_with_an_event__when_create_event_with_a_invalid_header__then_it_returns_400(
        self,
    ) -> None:
        # When
        header = {"HTTP_AUTHORIZATION": "invalid_token"}
        response = self.client.post(
            "/organizator-api/events/new",
            json.dumps(self.request_body),
            content_type="application/json",
            **header,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid token")

    def test__given_a_json_body_with_an_event__when_create_event_with_a_user_that_is_not_admin__then_it_returns_401(
        self,
    ) -> None:
        # When
        header = {"HTTP_AUTHORIZATION": f"{self.user_participant_token}"}
        response = self.client.post(
            "/organizator-api/events/new",
            json.dumps(self.request_body),
            content_type="application/json",
            **header,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"Only organizer admins can create events")

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
            b'[{"id": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc", "name": "HackUPC 2023", "url": "https://www.hackupc.com/", "description": "The biggest student hackathon in Europe", "start_date": "2023-05-12T16:00:00Z", "end_date": "2023-05-14T18:00:00Z", "location": "UPC Campus Nord", "header_image": "https://hackupc.com/ogimage.png", "deleted": false, "open_for_participants": true, "max_participants": 100, "expected_attrition_rate": 0.1, "students_only": true, "age_restrictions": 16}, {"id": "be0f4c18-4a7c-4c1e-8a62-fc50916b6c88", "name": "HackUPC 2022", "url": "https://www.hackupc.com/", "description": "The biggest student hackathon in Europe", "start_date": "2023-05-12T16:00:00Z", "end_date": "2023-05-14T18:00:00Z", "location": "UPC Campus Nord", "header_image": "https://hackupc.com/ogimage.png", "deleted": false, "open_for_participants": true, "max_participants": 100, "expected_attrition_rate": 0.1, "students_only": true, "age_restrictions": 16}]',
        )

    def test__given_event_deleted_in_db__when_get_all_events__then_it_returns_empty_list(
        self,
    ) -> None:
        # Given
        event = EventFactory().create(deleted_at=datetime.now())
        self.event_repository.create(event)

        # When
        response = self.client.get("/organizator-api/events/")

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"[]")

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
            b'[{"id": "be0f4c18-4a7c-4c1e-8a62-fc50916b6c88", "name": "HackUPC 2025", "url": "https://www.hackupc.com/", "description": "The biggest student hackathon in Europe", "start_date": "2025-05-12T16:00:00Z", "end_date": "2025-05-14T18:00:00Z", "location": "UPC Campus Nord", "header_image": "https://hackupc.com/ogimage.png", "deleted": false, "open_for_participants": true, "max_participants": 100, "expected_attrition_rate": 0.1, "students_only": true, "age_restrictions": 16}]',
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
            b'{"id": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc", "name": "HackUPC 2023", "url": "https://www.hackupc.com/", "description": "The biggest student hackathon in Europe", "start_date": "2023-05-12T16:00:00Z", "end_date": "2023-05-14T18:00:00Z", "location": "UPC Campus Nord", "header_image": "https://hackupc.com/ogimage.png", "deleted": false, "open_for_participants": true, "max_participants": 100, "expected_attrition_rate": 0.1, "students_only": true, "age_restrictions": 16}',
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
            "start_date": "17/11/2023 21:00",
            "end_date": "18/11/2023 05:00",
            "location": "Aula d'estudis Campus Nord",
            "header_image": "https://www.hacknights.dev/images/hacknight.png",
            "open_for_participants": False,
            "max_participants": 300,
            "expected_attrition_rate": 0.2,
            "students_only": True,
            "age_restrictions": 18,
        }

        # When
        headers = {"HTTP_AUTHORIZATION": f"{self.user_admin_token}"}
        response = self.client.post(
            "/organizator-api/events/update/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
            json.dumps(request_body),
            content_type="application/json",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"id": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc", "name": "HackNight Ep.VI", "url": "https://www.hacknights.dev", "description": "The best hack-night ever", "start_date": "2023-11-17T21:00:00Z", "end_date": "2023-11-18T05:00:00Z", "location": "Aula d\'estudis Campus Nord", "header_image": "https://www.hacknights.dev/images/hacknight.png", "deleted": false, "open_for_participants": true, "max_participants": 100, "expected_attrition_rate": 0.1, "students_only": true, "age_restrictions": 16}',
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
        self.assertEqual(event.open_for_participants, True)
        self.assertEqual(event.max_participants, 100)
        self.assertEqual(event.expected_attrition_rate, 0.1)
        self.assertEqual(event.students_only, True)
        self.assertEqual(event.age_restrictions, 16)

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
        headers = {"HTTP_AUTHORIZATION": f"{self.user_admin_token}"}
        response = self.client.post(
            "/organizator-api/events/update/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
            json.dumps(request_body),
            content_type="application/json",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"id": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc", "name": "HackUPC 2023", "url": "https://2023.hackupc.com/", "description": "The biggest student hackathon in Europe taking place in Barcelona", "start_date": "2023-05-12T16:00:00Z", "end_date": "2023-05-14T18:00:00Z", "location": "UPC Campus Nord", "header_image": "https://hackupc.com/ogimage.png", "deleted": false, "open_for_participants": true, "max_participants": 100, "expected_attrition_rate": 0.1, "students_only": true, "age_restrictions": 16}',
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
        headers = {"HTTP_AUTHORIZATION": f"{self.user_admin_token}"}
        response = self.client.post(
            "/organizator-api/events/update/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
            json.dumps(request_body),
            content_type="application/json",
            **headers,  # type: ignore
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
        headers = {"HTTP_AUTHORIZATION": f"{self.user_admin_token}"}
        response = self.client.post(
            "/organizator-api/events/update/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
            json.dumps(request_body),
            content_type="application/json",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"Event does not exist")

    def test__given_a_event__when_update_with_invalid_token__then_returns_400(
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
        headers = {"HTTP_AUTHORIZATION": "wrong_token"}
        response = self.client.post(
            "/organizator-api/events/update/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
            json.dumps(request_body),
            content_type="application/json",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid token")

    def test__given_a_event__when_update_with_a_user_that_is_not_admin__then_returns_401(
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
        headers = {"HTTP_AUTHORIZATION": f"{self.user_participant_token}"}
        response = self.client.post(
            "/organizator-api/events/update/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
            json.dumps(request_body),
            content_type="application/json",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"Only organizers can update events")

    def test__given_a_event__when_update_without_token__then_returns_401(self) -> None:
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
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"Unauthorized")

    def test__given_a_event__when_delete_event__then_the_event_is_deleted(
        self,
    ) -> None:
        # Given
        event = EventFactory().create()
        self.event_repository.create(event)

        # When
        headers = {"HTTP_AUTHORIZATION": f"{self.user_admin_token}"}
        response = self.client.post(
            "/organizator-api/events/delete/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Event updated correctly to be deleted")

    def test__given_no_event_in_db__when_delete_event__then_returns_404(
        self,
    ) -> None:
        # When
        headers = {"HTTP_AUTHORIZATION": f"{self.user_admin_token}"}
        response = self.client.post(
            "/organizator-api/events/delete/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"Event does not exist")

    def test__given_a_event__when_delete_with_invalid_token__then_returns_400(
        self,
    ) -> None:
        # When
        headers = {"HTTP_AUTHORIZATION": "invalid_token"}
        response = self.client.post(
            "/organizator-api/events/delete/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid token")

    def test__given_a_event__when_delete_with_no_token__then_returns_401(self) -> None:
        # When
        response = self.client.post(
            "/organizator-api/events/delete/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"Unauthorized")

    def test__given_a_event_and_a_participant_user__when_delete_with_token__then_returns_401(
        self,
    ) -> None:
        # Given
        event = EventFactory().create()
        self.event_repository.create(event)

        # When
        headers = {"HTTP_AUTHORIZATION": f"{self.user_participant_token}"}
        response = self.client.post(
            "/organizator-api/events/delete/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"Only organizer admins can delete events")

    def test__when_get_upcoming_events_with_application_information__then_return_unauthorized(self) -> None:
        # When
        response = self.client.get("/organizator-api/events/upcoming/applications")

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"Unauthorized")

    def test__when_get_upcoming_events_with_invalid_token__then_return_invalid_token(self) -> None:
        # When
        headers = {"HTTP_AUTHORIZATION": "invalid_token"}
        response = self.client.get(
            "/organizator-api/events/upcoming/applications",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid token")

    def test__given_no_user_in_bd__when_get_upcoming_events__then_return_user_does_not_exist(self) -> None:
        # When
        headers = {"HTTP_AUTHORIZATION": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"}
        response = self.client.get(
            "/organizator-api/events/upcoming/applications",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"User does not exist")

    def test__given_token_for_participant_user__when_get_upcoming_events__then_return_only_organizers_can_get_this_information(self) -> None:
        # When
        headers = {"HTTP_AUTHORIZATION": f"{self.user_participant_token}"}
        response = self.client.get(
            "/organizator-api/events/upcoming/applications",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"Only organizers can get this information")

    def test__given_token_for_admin_user_and_applications_in_events__when_get_upcoming_events__then_return_list_of_events_with_applications(self) -> None:
        # Given
        event = EventFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            name="HackUPC 2024",
            start_date=datetime(2025, 5, 12, 16, 0),
            end_date=datetime(2025, 5, 14, 18, 0),
        )
        event2 = EventFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00688"),
            name="HackUPC 2025",
            start_date=datetime(2026, 5, 12, 16, 0),
            end_date=datetime(2026, 5, 14, 18, 0),
        )

        self.event_repository.create(event)
        self.event_repository.create(event2)

        application = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            user=self.user_participant,
            event=event,
        )
        self.application_repository.create(application)

        application2 = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00688"),
            event=event,
        )
        self.application_repository.create(application2)

        application3 = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00681"),
            user=self.user_participant,
            event=event2,
        )
        self.application_repository.create(application3)

        application4 = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00681"),
            event=event2,
        )
        self.application_repository.create(application4)

        # When
        headers = {"HTTP_AUTHORIZATION": f"{self.user_admin_token}"}
        response = self.client.get(
            "/organizator-api/events/upcoming/applications",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'[{"name": "HackUPC 2024", "actual_participants_count": 2, "max_participants": 100, "expected_attrition_rate": 0.1}, {"name": "HackUPC 2025", "actual_participants_count": 2, "max_participants": 100, "expected_attrition_rate": 0.1}]')