import json
import uuid

from app.users.domain.models.user import UserRoles
from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory


class TestUserViews(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.event_repository.clear()








    def test__given_user_in_db__when_get_role_by_token__then_role_is_returned(
        self,
    ) -> None:
        # Given
        user = UserFactory().create(
            token=uuid.UUID("baad2fe5-0122-459b-9572-625c3351d6ac")
        )
        self.user_repository.create(user)

        # When
        headers = {"HTTP_Authorization": "baad2fe5-0122-459b-9572-625c3351d6ac"}
        response = self.client.get("/organizator-api/users/me/role", **headers)  # type: ignore

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"role": "Participant"}',
        )

    def test__given_user_in_db__when_get_role_by_token_without_header__then_unauthorized_is_returned(
        self,
    ) -> None:
        # Given
        user = UserFactory().create()
        self.user_repository.create(user)

        # When
        response = self.client.get("/organizator-api/users/me/role")

        # Then
        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.content,
            b"Unauthorized",
        )

    def test__when_get_role_by_token_with_a_invalid_token__then_invalid_token_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": "invalid_token"}
        response = self.client.get("/organizator-api/users/me/role", **headers)  # type: ignore

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid token")

    def test__given_non_existing_users_without_token__when_get_role_by_token__then_not_found_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": "8e0af048-073a-47e7-8de8-db7a17718e95"}
        response = self.client.get("/organizator-api/users/me/role", **headers)  # type: ignore

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"User does not exist")

    def test__given_user_in_db__when_get_by_username__then_user_is_returned(
        self,
    ) -> None:
        # Given
        user = UserFactory().create()
        self.user_repository.create(user)

        # When
        response = self.client.get("/organizator-api/users/carlotacb")

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"id": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc", "username": "carlotacb", "email": "carlota@hackupc.com", "first_name": "Carlota", "last_name": "Catot", "bio": "The user that is using this application", "profile_image": "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png", "role": "Participant"}',
        )

    def test__given_non_existing_user_in_db__when_get_by_username__then_not_found_is_returned(
        self,
    ) -> None:
        # When
        response = self.client.get("/organizator-api/users/charlie")

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"User does not exist")

    def test__given_user_in_db__when_update_user__then_user_is_updated(self) -> None:
        # Given
        token = "baad2fe5-0122-459b-9572-625c3351d6ac"
        user = UserFactory().create(token=uuid.UUID(token))
        self.user_repository.create(user)
        body = {
            "username": "charlie",
            "first_name": "Charlie",
            "last_name": "Brown",
            "bio": "I'm Charlie",
            "profile_image": "https://www.google.com",
        }

        # When
        header = {"HTTP_Authorization": token}
        response = self.client.post(
            "/organizator-api/users/update/me",
            json.dumps(body),
            content_type="application/json",
            **header,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"id": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc", "username": "charlie", "email": "carlota@hackupc.com", "first_name": "Charlie", "last_name": "Brown", "bio": "I\'m Charlie", "profile_image": "https://www.google.com", "role": "Participant"}',
        )

    def test__given_user_in_db__when_update_user_with_email__then_error_is_returned(
        self,
    ) -> None:
        # Given
        token = "baad2fe5-0122-459b-9572-625c3351d6ac"
        user = UserFactory().create(token=uuid.UUID(token))
        body = {"email": "carlota@hackupc.com"}

        # When
        header = {"HTTP_Authorization": token}
        response = self.client.post(
            "/organizator-api/users/update/me",
            json.dumps(body),
            content_type="application/json",
            **header,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"The email cannot be updated")

    def test__given_user_in_db__when_update_user_with_existing_username__then_error_is_returned(
        self,
    ) -> None:
        # Given
        token = "baad2fe5-0122-459b-9572-625c3351d6ac"
        user = UserFactory().create(token=uuid.UUID(token))
        self.user_repository.create(user)
        body = {"password": "carlotacb"}

        # When
        header = {"HTTP_Authorization": token}
        response = self.client.post(
            "/organizator-api/users/update/me",
            json.dumps(body),
            content_type="application/json",
            **header,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"The password cannot be updated")

    def test__given_user_in_db__when_update_user_with_a_existing_username__then_error_is_returned(
        self,
    ) -> None:
        # Given
        token = "baad2fe5-0122-459b-9572-625c3351d6ac"
        user = UserFactory().create(token=uuid.UUID(token))
        user2 = UserFactory().create(
            new_id=uuid.UUID("be0f4c18-4a7c-4c1e-8a62-fc50916b6c88"),
            email="carkbra@gmail.com",
            username="carkbra",
        )
        self.user_repository.create(user)
        self.user_repository.create(user2)
        body = {"username": "carkbra"}

        # When
        header = {"HTTP_Authorization": token}
        response = self.client.post(
            "/organizator-api/users/update/me",
            json.dumps(body),
            content_type="application/json",
            **header,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.content, b"User already exists")

    def test__given_no_user_in_db__when_update_a_non_existing_user__then_error_is_returned(
        self,
    ) -> None:
        # Given
        body = {
            "username": "charlie",
            "first_name": "Charlie",
            "last_name": "Brown",
            "bio": "I'm Charlie",
            "profile_image": "https://www.google.com",
        }

        # When
        header = {"HTTP_Authorization": "baad2fe5-0122-459b-9572-625c3351d6ac"}
        response = self.client.post(
            "/organizator-api/users/update/me",
            json.dumps(body),
            content_type="application/json",
            **header,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"User does not exist")

    def test__given_user_body__when_update_user_with_a_invalid_token__then_error_is_returned(
        self,
    ) -> None:
        # Given
        body = {"username": "charlie"}

        # When
        header = {"HTTP_Authorization": "wrong_token"}
        response = self.client.post(
            "/organizator-api/users/update/me",
            json.dumps(body),
            content_type="application/json",
            **header,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid token")

    def test_given_user_body__when_update_without_header__then_unauthorized_is_returned(
        self,
    ) -> None:
        # Given
        body = {"username": "charlie"}

        # When
        response = self.client.post(
            "/organizator-api/users/update/me",
            json.dumps(body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.content, b"Unauthorized")

    def test__given_user_in_db_and_correct_body__when_login_endpoint_is_called__then_token_is_created(
        self,
    ) -> None:
        # Given
        user = UserFactory().create()
        self.user_repository.create(user)
        body = {"username": user.username, "password": "123456"}

        # When
        response = self.client.post(
            "/organizator-api/users/login",
            json.dumps(body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 200)

    def test__given_user_in_db_and_body_with_incorrect_password__when_when_login_endpoint_is_called__then_error_is_returned(
        self,
    ) -> None:
        # Given
        user = UserFactory().create()
        self.user_repository.create(user)
        body = {"username": user.username, "password": "wrong password"}

        # When
        response = self.client.post(
            "/organizator-api/users/login",
            json.dumps(body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"Invalid password")

    def test__given_a_boy_with_a_unexisting_username__when_login_endpoint_is_called__then_error_is_returned(
        self,
    ) -> None:
        # Given
        body = {"username": "unexisting user", "password": "password"}

        # When
        response = self.client.post(
            "/organizator-api/users/login",
            json.dumps(body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"User does not exist")

    def test__given_a_unexpected_body_without_username__when_login_endpoint_is_called__then_error_is_returned(
        self,
    ) -> None:
        # Given
        body = {"password": "password"}

        # When
        response = self.client.post(
            "/organizator-api/users/login",
            json.dumps(body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Username is required")

    def test__given_a_unexpected_body_without_password__when_login_endpoint_is_called__then_error_is_returned(
        self,
    ) -> None:
        # Given
        body = {"username": "username"}

        # When
        response = self.client.post(
            "/organizator-api/users/login",
            json.dumps(body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Password is required")

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
