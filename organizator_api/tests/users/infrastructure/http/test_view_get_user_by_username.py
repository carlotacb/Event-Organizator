from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory


class TestViewGetUserByUsername(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository.clear()
        user = UserFactory().create()
        self.user_repository.create(user)

    def test__given_non_existing_user_in_db__when_get_by_username__then_not_found_is_returned(
        self,
    ) -> None:
        # When
        response = self.client.get("/organizator-api/users/charlie")

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"User does not exist")

    def test__given_user_in_db__when_get_by_username__then_user_is_returned(
        self,
    ) -> None:
        # When
        response = self.client.get("/organizator-api/users/carlotacb")

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"id": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc", "username": "carlotacb", "email": "carlota@hackupc.com", "first_name": "Carlota", "last_name": "Catot", "bio": "The user that is using this application", "profile_image": "profile_picture.png", "role": "Participant", "date_of_birth": "07/05/1996", "study": true, "work": false, "university": "Universitat Polit\\u00e8cnica de Catalunya", "degree": "Computer Science", "expected_graduation": "01/05/2024", "current_job_role": "", "tshirt": "", "gender": "", "alimentary_restrictions": "", "github": "", "linkedin": "", "devpost": "", "webpage": ""}',
        )
