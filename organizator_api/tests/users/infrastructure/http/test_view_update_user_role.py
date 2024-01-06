import json
import uuid

from app.users.domain.models.user import UserRoles
from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory


class TestViewUpdateUserRole(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository.clear()
        self.token_user_admin = "60d99f6a-7fb6-4bec-87da-bc5c8a44fb4d"
        user = UserFactory().create(
            token=uuid.UUID(self.token_user_admin), role=UserRoles.ORGANIZER_ADMIN
        )
        self.user_repository.create(user)

        self.token_user_participant = "60d99f6a-7fb6-4bec-87da-bc5c8a44fb5c"
        user = UserFactory().create(
            new_id=uuid.UUID("60d99f6a-7fb6-4bec-87da-bc5c8a44fb4e"),
            email="carlota@test.com",
            username="charlie",
            token=uuid.UUID(self.token_user_participant),
            role=UserRoles.PARTICIPANT,
        )
        self.user_repository.create(user)

    def test__given_body_to_change_role__when_update_role_without_header__then_unauthorized_is_returned(
        self,
    ) -> None:
        # Given
        body = {"role": "ORGANIZER"}

        # When
        response = self.client.post(
            "/organizator-api/users/update/role/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
            json.dumps(body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"Unauthorized")

    def test__given_body_to_change_role__when_update_role_with_a_invalid_token_in_header__then_invalid_token_is_returned(
        self,
    ) -> None:
        # Given
        body = {"role": "ORGANIZER"}

        # When
        headers = {"HTTP_Authorization": "invalid_token"}
        response = self.client.post(
            "/organizator-api/users/update/role/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
            json.dumps(body),
            content_type="application/json",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid token")

    def test__given_a_invalid_body__when_update_role__then_unexpected_body_is_returned(
        self,
    ) -> None:
        # Given
        body = {"test": "test"}

        # When
        headers = {"HTTP_Authorization": self.token_user_admin}
        response = self.client.post(
            "/organizator-api/users/update/role/60d99f6a-7fb6-4bec-87da-bc5c8a44fb4e",
            json.dumps(body),
            content_type="application/json",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.content,
            b"Unexpected body",
        )

    def test__given_body_to_modify_participant_to_organizer__when_update_role__then_user_does_not_exist_is_returned(
        self,
    ) -> None:
        # Given
        body = {"role": "ORGANIZER"}

        # When
        headers = {"HTTP_Authorization": self.token_user_admin}
        response = self.client.post(
            "/organizator-api/users/update/role/ef6f6fb3-ba12-43dd-a0da-95de8125b1cd",
            json.dumps(body),
            content_type="application/json",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.content,
            b"User does not exist",
        )

    def test__given_body_to_modify_participant_to_organizer__when_update_role_by_organizer_user__then_only_authorized_to_organizer_admin_is_returned(
        self,
    ) -> None:
        # Given
        body = {"role": "ORGANIZER"}

        # When
        headers = {"HTTP_Authorization": self.token_user_participant}
        response = self.client.post(
            "/organizator-api/users/update/role/60d99f6a-7fb6-4bec-87da-bc5c8a44fb4e",
            json.dumps(body),
            content_type="application/json",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.content,
            b"Only authorized to organizer admin",
        )

    def test__given_body_with_a_invalid_role__when_update_role_by_admin__then_invalid_role_is_returned(
        self,
    ) -> None:
        # Given
        body = {"role": "INVALID_ROLE"}

        # When
        headers = {"HTTP_Authorization": self.token_user_admin}
        response = self.client.post(
            "/organizator-api/users/update/role/60d99f6a-7fb6-4bec-87da-bc5c8a44fb4e",
            json.dumps(body),
            content_type="application/json",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content,
            b"Invalid role",
        )

    def test__given_body_with_organizer_as_new_role__when_update_participant_role_by_admin_user__then_it_updates(
        self,
    ) -> None:
        # Given
        body = {"role": "ORGANIZER"}

        # When
        headers = {"HTTP_Authorization": self.token_user_admin}
        response = self.client.post(
            "/organizator-api/users/update/role/60d99f6a-7fb6-4bec-87da-bc5c8a44fb4e",
            json.dumps(body),
            content_type="application/json",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"id": "60d99f6a-7fb6-4bec-87da-bc5c8a44fb4e", "username": "charlie", "email": "carlota@test.com", "first_name": "Carlota", "last_name": "Catot", "bio": "The user that is using this application", "profile_image": "profile_picture.png", "role": "Organizer", "date_of_birth": "07/05/1996", "study": true, "work": false, "university": "Universitat Polit\\u00e8cnica de Catalunya", "degree": "Computer Science", "expected_graduation": "01/05/2024", "current_job_role": "", "tshirt": "", "gender": "", "alimentary_restrictions": "", "github": "", "linkedin": "", "devpost": "", "webpage": ""}',
        )
