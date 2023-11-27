import json

from tests.api_tests import ApiTests


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
