import json
import uuid

from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory


class TestUserViews(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.event_repository.clear()

    def test__given_unexpected_body__when_create_user__then_bad_request_is_returned(
        self,
    ) -> None:
        # Given
        body = {}  # type: ignore

        # When
        response = self.client.post(
            "/organizator-api/users/new",
            json.dumps(body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Unexpected body")

    def test__given_user_already_exists__when_create_user__then_conflict_is_returned(
        self,
    ) -> None:
        # Given
        body = {
            "email": "carlota@hackpc.com",
            "password": "12345678",
            "first_name": "Carlota",
            "last_name": "Catot",
            "username": "carlota",
            "bio": "I'm Carlota",
            "profile_image": "https://www.google.com",
        }
        body2 = {
            "email": "carkbra@hackupc.com",
            "password": "12345678",
            "first_name": "Carlota",
            "last_name": "Catot",
            "username": "carlota",
            "bio": "I'm Carlota",
            "profile_image": "https://www.google.com",
        }

        # When
        self.client.post(
            "/organizator-api/users/new",
            json.dumps(body),
            content_type="application/json",
        )
        response = self.client.post(
            "/organizator-api/users/new",
            json.dumps(body2),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.content, b"User already exists")

    def test__given_a_json_body_with_a_user__when_creat_user__then_the_user_is_created_and_stored_in_db(
        self,
    ) -> None:
        # Given
        body = {
            "email": "carlota@hackupc.com",
            "password": "12345678",
            "first_name": "Carlota",
            "last_name": "Catot",
            "username": "carlota",
            "bio": "I'm Carlota",
            "profile_image": "https://www.google.com",
        }

        # When
        response = self.client.post(
            "/organizator-api/users/new",
            json.dumps(body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content, b"User created correctly")

        self.assertEqual(len(self.user_repository.get_all()), 1)
        user = self.user_repository.get_all().pop()
        self.assertEqual(user.email, "carlota@hackupc.com")
        self.assertEqual(user.password, "12345678")
        self.assertEqual(user.first_name, "Carlota")
        self.assertEqual(user.last_name, "Catot")
        self.assertEqual(user.username, "carlota")
        self.assertEqual(user.bio, "I'm Carlota")
        self.assertEqual(user.profile_image, "https://www.google.com")

    def test__given_no_users_in_db__when_get_all_users__then_empty_list_is_returned(
        self,
    ) -> None:
        # When
        response = self.client.get("/organizator-api/users/")

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"[]")

    def test__given_users_in_db__when_get_all_users__then_all_users_are_returned(
        self,
    ) -> None:
        # Given
        user = UserFactory().create()
        user2 = UserFactory().create(
            new_id=uuid.UUID("be0f4c18-4a7c-4c1e-8a62-fc50916b6c88"),
            email="carkbra@gmail.com",
            username="carkbra",
        )
        self.user_repository.create(user)
        self.user_repository.create(user2)

        # When
        response = self.client.get("/organizator-api/users/")

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'[{"id": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc", "username": "carlotacb", "email": "carlota@hackupc.com", "first_name": "Carlota", "last_name": "Catot", "bio": "The user that is using this application", "profile_image": "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"}, {"id": "be0f4c18-4a7c-4c1e-8a62-fc50916b6c88", "username": "carkbra", "email": "carkbra@gmail.com", "first_name": "Carlota", "last_name": "Catot", "bio": "The user that is using this application", "profile_image": "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"}]',
        )

    def test__given_user_in_db__when_get_by_id__then_user_is_returned(self) -> None:
        # Given
        user = UserFactory().create()
        self.user_repository.create(user)

        # When
        response = self.client.get(
            "/organizator-api/users/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"id": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc", "username": "carlotacb", "email": "carlota@hackupc.com", "first_name": "Carlota", "last_name": "Catot", "bio": "The user that is using this application", "profile_image": "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"}',
        )

    def test__given_non_existing_user_in_db__when_get_by_id__then_not_found_is_returned(
        self,
    ) -> None:
        # When
        response = self.client.get(
            "/organizator-api/users/ef6f6fb3-ba12-43dd-a0da-95de8125b1cd"
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"User does not exist")

    def test__given_user_in_db__when_get_me__then_user_is_returned(self) -> None:
        # Given
        user = UserFactory().create(token=uuid.UUID("baad2fe5-0122-459b-9572-625c3351d6ac"))
        self.user_repository.create(user)

        # When
        headers = {"Authorization": user.token}
        response = self.client.get(
            "/organizator-api/users/me",
            **headers
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"id": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc", "username": "carlotacb", "email": "carlota@hackupc.com", "first_name": "Carlota", "last_name": "Catot", "bio": "The user that is using this application", "profile_image": "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"}',
        )
    def test__given_user_in_db__when_get_me_without_header__then_user_is_returned(self) -> None:
        # Given
        user = UserFactory().create()
        self.user_repository.create(user)

        # When
        response = self.client.get(
            "/organizator-api/users/me"
        )

        # Then
        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.content,
            b'Unauthorized',
        )

    def test__given_non_existing_users_without_token__when_get_me__then_not_found_is_returned(
        self,
    ) -> None:
        # When
        response = self.client.get(
            "/organizator-api/users/me"
        )

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
            b'{"id": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc", "username": "carlotacb", "email": "carlota@hackupc.com", "first_name": "Carlota", "last_name": "Catot", "bio": "The user that is using this application", "profile_image": "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"}',
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
        user = UserFactory().create()
        self.user_repository.create(user)
        body = {
            "username": "charlie",
            "first_name": "Charlie",
            "last_name": "Brown",
            "bio": "I'm Charlie",
            "profile_image": "https://www.google.com",
        }

        # When
        response = self.client.post(
            "/organizator-api/users/update/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
            json.dumps(body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"id": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc", "username": "charlie", "email": "carlota@hackupc.com", "first_name": "Charlie", "last_name": "Brown", "bio": "I\'m Charlie", "profile_image": "https://www.google.com"}',
        )

    def test__given_user_in_db__when_update_user_with_email__then_error_is_returned(
        self,
    ) -> None:
        # Given
        user = UserFactory().create()
        self.user_repository.create(user)
        body = {"email": "carlota@hackupc.com"}

        # When
        response = self.client.post(
            "/organizator-api/users/update/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
            json.dumps(body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"The email cannot be updated")

    def test__given_user_in_db__when_update_user_with_existing_username__then_error_is_returned(
        self,
    ) -> None:
        # Given
        user = UserFactory().create()
        self.user_repository.create(user)
        body = {"password": "carlotacb"}

        # When
        response = self.client.post(
            "/organizator-api/users/update/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
            json.dumps(body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"The password cannot be updated")

    def test__given_user_in_db__when_update_user_with_a_existing_username__then_error_is_returned(
        self,
    ) -> None:
        # Given
        user = UserFactory().create()
        user2 = UserFactory().create(
            new_id=uuid.UUID("be0f4c18-4a7c-4c1e-8a62-fc50916b6c88"),
            email="carkbra@gmail.com",
            username="carkbra",
        )
        self.user_repository.create(user)
        self.user_repository.create(user2)
        body = {"username": "carkbra"}

        # When
        response = self.client.post(
            "/organizator-api/users/update/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
            json.dumps(body),
            content_type="application/json",
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
        response = self.client.post(
            "/organizator-api/users/update/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc",
            json.dumps(body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"User does not exist")

    def test__given_user_in_db_and_correct_body__when_login_endpoint_is_called__then_token_is_created(
        self,
    ) -> None:
        # Given
        user = UserFactory().create()
        self.user_repository.create(user)
        body = {"username": user.username, "password": user.password}

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
