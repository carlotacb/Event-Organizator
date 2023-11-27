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
