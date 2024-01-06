import json
import uuid

from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory


class TestViewLogin(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository.clear()
        user = UserFactory().create()
        self.user_repository.create(user)

    def test__given_a_body_with_only_password__when_login__then_username_is_required_is_returned(
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
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.content, b"Username is required")

    def test__given_a_body_with_only_username__when_login__then_password_is_required_is_returned(
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
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.content, b"Password is required")

    def test__given_a_body_with_a_non_existing_username_and_password__when_login__then_user_does_not_exist_is_returned(
        self,
    ) -> None:
        # Given
        body = {"username": "fake user", "password": "password"}

        # When
        response = self.client.post(
            "/organizator-api/users/login",
            json.dumps(body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"User does not exist")

    def test__given_a_body_with_incorrect_password__when_login__then_invalid_password_is_returned(
        self,
    ) -> None:
        # Given
        body = {"username": "carlotacb", "password": "wrong password"}

        # When
        response = self.client.post(
            "/organizator-api/users/login",
            json.dumps(body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"Invalid password")

    def test__given_a_body_with_correct_username_and_password__when_login__then_token_is_created(
        self,
    ) -> None:
        # Given
        body = {"username": "carlotacb", "password": "123456"}

        # When
        response = self.client.post(
            "/organizator-api/users/login",
            json.dumps(body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.user_repository.get_all()[0].token, uuid.UUID(response.json()["token"])
        )
