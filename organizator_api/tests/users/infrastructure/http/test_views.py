import json
import uuid

from app.users.domain.models.user import UserRoles
from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory


class TestUserViews(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.event_repository.clear()








    def test__given_a_user_with_a_token__when_logout_endpoint_is_called__then_token_is_deleted(
        self,
    ) -> None:
        # Given
        token_for_user = uuid.UUID("60d99f6a-7fb6-4bec-87da-bc5c8a44fb4d")
        user = UserFactory().create(token=token_for_user)
        self.user_repository.create(user)

        # When
        headers = {"HTTP_Authorization": "60d99f6a-7fb6-4bec-87da-bc5c8a44fb4d"}
        response = self.client.post("/organizator-api/users/logout", **headers)  # type: ignore

        # Then
        self.assertEqual(response.status_code, 200)

    def test__given_a_user_with_token__when_logout_endpoint_is_called_without_header__then_unauthorized_is_returned(
        self,
    ) -> None:
        # Given
        token_for_user = uuid.UUID("60d99f6a-7fb6-4bec-87da-bc5c8a44fb4d")
        user = UserFactory().create(token=token_for_user)
        self.user_repository.create(user)

        # When
        response = self.client.post("/organizator-api/users/logout")

        # Then
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.content, b"Unauthorized")

    def test__when_logout_with_invalid_token__then_invalid_token_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": "invalid_token"}
        response = self.client.post("/organizator-api/users/logout", **headers)  # type: ignore

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid token")








    def test__given_a_user_with_token_and_admin_and_a_participant_user__when_update_participant_role_to_organizer__then_it_updates(
        self,
    ) -> None:
        # Given
        token_user = "60d99f6a-7fb6-4bec-87da-bc5c8a44fb4d"
        token_for_user = uuid.UUID(token_user)
        user = UserFactory().create(
            token=token_for_user, role=UserRoles.ORGANIZER_ADMIN
        )
        self.user_repository.create(user)
        participant_user = UserFactory().create(
            new_id=uuid.UUID("60d99f6a-7fb6-4bec-87da-bc5c8a44fb4e"),
            email="carlota2@hackupc.com",
            username="charlie",
        )
        self.user_repository.create(participant_user)

        # When
        headers = {"HTTP_Authorization": token_user}
        body = {"role": "ORGANIZER"}
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
            b'{"id": "60d99f6a-7fb6-4bec-87da-bc5c8a44fb4e", "username": "charlie", "email": "carlota2@hackupc.com", "first_name": "Carlota", "last_name": "Catot", "bio": "The user that is using this application", "profile_image": "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png", "role": "Organizer"}',
        )

    def test__given_a_user_in_bd__when_update_role_to_organizer_without_header__then_unauthorized_is_returned(
        self,
    ) -> None:
        # Given
        token_user = "60d99f6a-7fb6-4bec-87da-bc5c8a44fb4d"
        token_for_user = uuid.UUID(token_user)
        user = UserFactory().create(
            token=token_for_user, role=UserRoles.ORGANIZER_ADMIN
        )
        self.user_repository.create(user)

        # When
        body = {"role": "ORGANIZER"}
        response = self.client.post(
            "/organizator-api/users/update/role/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
            json.dumps(body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.content, b"Unauthorized")

    def test__given_a_user_in_bd__when_update_participant_with_a_invalid_header__then_invalid_token_is_returned(
        self,
    ) -> None:
        # Given
        user = UserFactory().create()
        self.user_repository.create(user)

        # When
        headers = {"HTTP_Authorization": "60d99f6a-7fb6-4bec-87da-bc5c8a44f"}
        body = {"role": "ORGANIZER"}
        response = self.client.post(
            "/organizator-api/users/update/role/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
            json.dumps(body),
            content_type="application/json",
            **headers,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid token")

    def test__given_a_user_in_bd__when_update_participant_with_a_invalid_body__then_unexpected_body_is_returned(
        self,
    ) -> None:
        # Given
        token_user = "60d99f6a-7fb6-4bec-87da-bc5c8a44fb4d"
        token_for_user = uuid.UUID(token_user)
        user = UserFactory().create(
            new_id=uuid.UUID("60d99f6a-7fb6-4bec-87da-bc5c8a44fb4e"),
            token=token_for_user,
            role=UserRoles.ORGANIZER_ADMIN,
        )
        self.user_repository.create(user)

        # When
        headers = {"HTTP_Authorization": token_user}
        body = {"test": "test"}
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
            b"Unexpected body",
        )

    def test__given_a_user_in_bd__when_update_participant_with_a_invalid_role__then_invalid_role_is_returned(
        self,
    ) -> None:
        # Given
        token_user = "60d99f6a-7fb6-4bec-87da-bc5c8a44fb4d"
        token_for_user = uuid.UUID(token_user)
        user = UserFactory().create(
            new_id=uuid.UUID("60d99f6a-7fb6-4bec-87da-bc5c8a44fb4e"),
            token=token_for_user,
            role=UserRoles.ORGANIZER_ADMIN,
        )
        self.user_repository.create(user)

        # When
        headers = {"HTTP_Authorization": token_user}
        body = {"role": "INVALID_ROLE"}
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

    def test__given_a_user_in_bd__when_update_participant_with_a_invalid_user__then_user_does_not_exist_is_returned(
        self,
    ) -> None:
        # Given
        token_user = "60d99f6a-7fb6-4bec-87da-bc5c8a44fb4d"
        token_for_user = uuid.UUID(token_user)
        user = UserFactory().create(
            new_id=uuid.UUID("60d99f6a-7fb6-4bec-87da-bc5c8a44fb4e"),
            token=token_for_user,
            role=UserRoles.ORGANIZER_ADMIN,
        )
        self.user_repository.create(user)

        # When
        headers = {"HTTP_Authorization": token_user}
        body = {"role": "ORGANIZER"}
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

    def test__given_a_participant_user_in_db__when_update_participant__then_only_authorized_to_organizer_admin_is_returned(
        self,
    ) -> None:
        # Given
        token_user = "60d99f6a-7fb6-4bec-87da-bc5c8a44fb4d"
        token_for_user = uuid.UUID(token_user)
        user = UserFactory().create(
            new_id=uuid.UUID("60d99f6a-7fb6-4bec-87da-bc5c8a44fb4e"),
            token=token_for_user,
            role=UserRoles.PARTICIPANT,
        )
        self.user_repository.create(user)

        # When
        headers = {"HTTP_Authorization": token_user}
        body = {"role": "ORGANIZER"}
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
