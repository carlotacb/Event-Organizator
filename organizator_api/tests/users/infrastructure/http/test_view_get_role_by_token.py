import uuid

from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory


class TestViewGetMyRole(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository.clear()
        self.token = "baad2fe5-0122-459b-9572-625c3351d6ac"
        user = UserFactory().create(token=uuid.UUID(self.token))
        self.user_repository.create(user)

    def test__given_user_in_db__when_get_role_by_token_without_header__then_unauthorized_is_returned(
        self,
    ) -> None:
        # When
        response = self.client.get("/organizator-api/users/me/role")

        # Then
        self.assertEqual(response.status_code, 401)
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

    def test__given_user_in_db__when_get_role_by_token__then_role_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": self.token}
        response = self.client.get("/organizator-api/users/me/role", **headers)  # type: ignore

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"role": "Participant"}',
        )



