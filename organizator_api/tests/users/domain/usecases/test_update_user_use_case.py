import uuid

from app.users.application.requests import UpdateUserRequest
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
            profile_image="https://www.hacknights.dev/images/hacknight.png",
        )

        # When
        user = UpdateUserUseCase().execute(token=self.user_token, user=user_data)

        # Then
        self.assertEqual("carlota", user.username)
        self.assertEqual("Carlota", user.first_name)
        self.assertEqual("Catot", user.last_name)
        self.assertEqual("I'm a cat", user.bio)
        self.assertEqual(
            "https://www.hacknights.dev/images/hacknight.png", user.profile_image
        )
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
        user = UpdateUserUseCase().execute(token=self.user_token, user=user_data)

        # Then
        self.assertEqual("carlotacb", user.username)
        self.assertEqual("Carlota", user.first_name)
        self.assertEqual("Catot", user.last_name)
        self.assertEqual("The user that is using this application", user.bio)
        self.assertEqual(
            "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png",
            user.profile_image,
        )
        self.assertEqual(self.user_token, user.token)

    def test__given_update_user_request_with_only_bio__when_update_user__then_the_user_is_updated(
        self,
    ) -> None:
        # Given
        user_data = UpdateUserRequest(
            bio="I'm the beeest",
        )

        # When
        user = UpdateUserUseCase().execute(token=self.user_token, user=user_data)

        # Then
        self.assertEqual("carlotacb", user.username)
        self.assertEqual("Carlota", user.first_name)
        self.assertEqual("Catot", user.last_name)
        self.assertEqual("I'm the beeest", user.bio)
        self.assertEqual(
            "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png",
            user.profile_image,
        )
        self.assertEqual(self.user_token, user.token)

    def test__given_update_user_request_with_username_with_uppercase_letters__when_update_user__then_the_user_is_updated_and_the_user_is_lowercase(
        self,
    ) -> None:
        # Given
        user_data = UpdateUserRequest(
            username="CarlotaCB24",
        )

        # When
        user = UpdateUserUseCase().execute(token=self.user_token, user=user_data)

        # Then
        self.assertEqual("carlotacb24", user.username)
