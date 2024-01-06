import uuid
from datetime import datetime, timezone

from app.users.application.requests import UpdateUserRequest
from app.users.domain.models.user import UserRoles, GenderOptions
from app.users.domain.usecases.update_user_use_case import UpdateUserUseCase
from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory


class TestUpdateUserUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository.clear()
        self.user_token = uuid.UUID("5b90906e-2894-467d-835e-3e4fbe42af9f")
        user = UserFactory().create(token=self.user_token)
        self.user_repository.create(user)

    def test__given_update_user_request__when_update_user__then_the_user_is_updated(
        self,
    ) -> None:
        # Given
        user_data = UpdateUserRequest(
            username="carlota",
            first_name="Carlota",
            last_name="Catot",
            bio="I'm a cat",
            profile_image="profile_picture_2.png",
        )

        # When
        user = UpdateUserUseCase().execute(token=self.user_token, user_data=user_data)

        # Then
        self.assertEqual("carlota", user.username)
        self.assertEqual("Carlota", user.first_name)
        self.assertEqual("Catot", user.last_name)
        self.assertEqual("I'm a cat", user.bio)
        self.assertEqual("profile_picture_2.png", user.profile_image)
        self.assertEqual("carlota@hackupc.com", user.email)
        self.assertEqual(self.user_token, user.token)

    def test__given_update_user_request_with_empty_fields__when_update_user__then_the_user_is_not_updated(
        self,
    ) -> None:
        # Given
        user_data = UpdateUserRequest(
            username="",
            first_name="",
            last_name="",
            bio="",
            profile_image="",
        )

        # When
        user = UpdateUserUseCase().execute(token=self.user_token, user_data=user_data)

        # Then
        self.assertEqual("carlotacb", user.username)
        self.assertEqual("Carlota", user.first_name)
        self.assertEqual("Catot", user.last_name)
        self.assertEqual("The user that is using this application", user.bio)
        self.assertEqual("profile_picture.png", user.profile_image)
        self.assertEqual(self.user_token, user.token)

    def test__given_update_user_request_with_only_bio__when_update_user__then_the_user_is_updated(
        self,
    ) -> None:
        # Given
        user_data = UpdateUserRequest(
            bio="I'm the beeest",
        )

        # When
        user = UpdateUserUseCase().execute(token=self.user_token, user_data=user_data)

        # Then
        self.assertEqual("carlotacb", user.username)
        self.assertEqual("Carlota", user.first_name)
        self.assertEqual("Catot", user.last_name)
        self.assertEqual("I'm the beeest", user.bio)
        self.assertEqual("profile_picture.png", user.profile_image)
        self.assertEqual(self.user_token, user.token)

    def test__given_update_user_request_with_username_with_uppercase_letters__when_update_user__then_the_user_is_updated_and_the_user_is_lowercase(
        self,
    ) -> None:
        # Given
        user_data = UpdateUserRequest(
            username="CarlotaCB24",
        )

        # When
        user = UpdateUserUseCase().execute(token=self.user_token, user_data=user_data)

        # Then
        self.assertEqual("carlotacb24", user.username)

    def test__given_user_with_basic_information_and_update_user_request_with_the_rest_of_information__when_update_user__then_the_user_is_updated_with_all_the_information(
        self,
    ) -> None:
        # Given
        user_data = UpdateUserRequest(
            tshirt="XS",
            alimentary_restrictions="No restrictions",
            gender="FEMALE",
            github="http://github.com/carlotacb",
            linkedin="http://linkedin.com/in/carlotacb",
            devpost="http://devpost.com/carlotacb",
            webpage="http://carlotacb.dev",
        )

        # When
        user = UpdateUserUseCase().execute(token=self.user_token, user_data=user_data)

        # Then
        self.assertEqual("carlota@hackupc.com", user.email)
        self.assertEqual("Carlota", user.first_name)
        self.assertEqual("Catot", user.last_name)
        self.assertEqual("carlotacb", user.username)
        self.assertEqual("The user that is using this application", user.bio)
        self.assertEqual("profile_picture.png", user.profile_image)
        self.assertEqual(UserRoles.PARTICIPANT, user.role)
        self.assertEqual(datetime(1996, 5, 7, 0, 0), user.date_of_birth)
        self.assertEqual(True, user.study)
        self.assertEqual(False, user.work)
        self.assertEqual("Universitat Politècnica de Catalunya", user.university)
        self.assertEqual("Computer Science", user.degree)
        self.assertEqual(datetime(2024, 5, 1, 0, 0), user.expected_graduation)
        self.assertEqual(None, user.current_job_role)
        self.assertEqual("XS", user.tshirt.value)  # type: ignore
        self.assertEqual(GenderOptions.FEMALE, user.gender)
        self.assertEqual("No restrictions", user.alimentary_restrictions)
        self.assertEqual("http://github.com/carlotacb", user.github)
        self.assertEqual("http://linkedin.com/in/carlotacb", user.linkedin)
        self.assertEqual("http://devpost.com/carlotacb", user.devpost)
        self.assertEqual("http://carlotacb.dev", user.webpage)
        self.assertEqual(self.user_token, user.token)
