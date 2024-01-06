import uuid

from app.users.domain.models.user import TShirtSizes, GenderOptions
from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory


class TestViewGetUserById(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository.clear()

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
            b'{"id": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc", "username": "carlotacb", "email": "carlota@hackupc.com", "first_name": "Carlota", "last_name": "Catot", "bio": "The user that is using this application", "profile_image": "profile_picture.png", "role": "Participant", "date_of_birth": "07/05/1996", "study": true, "work": false, "university": "Universitat Polit\\u00e8cnica de Catalunya", "degree": "Computer Science", "expected_graduation": "01/05/2024", "current_job_role": "", "tshirt": "", "gender": "", "alimentary_restrictions": "", "github": "", "linkedin": "", "devpost": "", "webpage": ""}',
        )

    def test__given_user_in_db_with_all_the_information__when_get_by_id__then_all_the_information_is_returned(
        self,
    ) -> None:
        # Given
        user = UserFactory().create(
            token=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"),
            tshirt=TShirtSizes.XS,
            gender=GenderOptions.FEMALE,
            alimentary_restrictions="No allergies",
            github="http://github.com/carlotacb",
            linkedin="http://linkedin.com/carlotacb",
            devpost="http://devpost.com/carlotacb",
            webpage="http://carlotacb.dev",
        )
        self.user_repository.create(user)

        # When
        response = self.client.get(
            "/organizator-api/users/ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"id": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc", "username": "carlotacb", "email": "carlota@hackupc.com", "first_name": "Carlota", "last_name": "Catot", "bio": "The user that is using this application", "profile_image": "profile_picture.png", "role": "Participant", "date_of_birth": "07/05/1996", "study": true, "work": false, "university": "Universitat Polit\\u00e8cnica de Catalunya", "degree": "Computer Science", "expected_graduation": "01/05/2024", "current_job_role": "", "tshirt": "XS", "gender": "Female", "alimentary_restrictions": "No allergies", "github": "http://github.com/carlotacb", "linkedin": "http://linkedin.com/carlotacb", "devpost": "http://devpost.com/carlotacb", "webpage": "http://carlotacb.dev"}',
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
