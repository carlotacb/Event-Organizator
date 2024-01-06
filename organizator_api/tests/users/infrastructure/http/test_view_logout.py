import uuid

from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory


class TestViewLogout(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository.clear()
        self.token_for_user = "60d99f6a-7fb6-4bec-87da-bc5c8a44fb4d"
        user = UserFactory().create(token=uuid.UUID(self.token_for_user))
        self.user_repository.create(user)

    def test__when_logout_without_header__then_unauthorized_is_returned(
        self,
    ) -> None:
        # When
        response = self.client.post("/organizator-api/users/logout")

        # Then
        self.assertEqual(response.status_code, 401)
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

    def test__given_user_with_token_in_db__when_logout__then_token_is_deleted(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": self.token_for_user}
        response = self.client.post("/organizator-api/users/logout", **headers)  # type: ignore

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user_repository.get_all()[0].token, None)
