import uuid

from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory


class TestViewGetMe(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.event_repository.clear()
        self.token = "baad2fe5-0122-459b-9572-625c3351d6ac"
        user = UserFactory().create(
            token=uuid.UUID(self.token),
        )
        self.user_repository.create(user)

    def test__given_user_in_db__when_get_me_without_header__then_user_is_returned(
        self,
    ) -> None:
        # When
        response = self.client.get("/organizator-api/users/me")

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.content,
            b"Unauthorized",
        )

    def test__given_user_in_db__when_get_me_is_called_with_a_invalid_token__then_invalid_token_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": "invalid_token"}
        response = self.client.get("/organizator-api/users/me", **headers)  # type: ignore

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content,
            b"Invalid token",
        )

    def test__given_non_existing_users_without_token__when_get_me__then_not_found_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": "8e0af048-073a-47e7-8de8-db7a17718e95"}
        response = self.client.get("/organizator-api/users/me", **headers)  # type: ignore

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"User does not exist")

    def test__given_user_in_db__when_get_me__then_user_is_returned(self) -> None:
        # When
        headers = {"HTTP_Authorization": self.token}
        response = self.client.get("/organizator-api/users/me", **headers)  # type: ignore

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"id": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc", "username": "carlotacb", "email": "carlota@hackupc.com", "first_name": "Carlota", "last_name": "Catot", "bio": "The user that is using this application", "profile_image": "profile_picture.png", "role": "Participant", "date_of_birth": "07/05/1996", "study": true, "work": false, "university": "Universitat Polit\\u00e8cnica de Catalunya", "degree": "Computer Science", "expected_graduation": "01/05/2024", "current_job_role": "", "tshirt": "", "gender": "", "alimentary_restrictions": "", "github": "", "linkedin": "", "devpost": "", "webpage": ""}',
        )
