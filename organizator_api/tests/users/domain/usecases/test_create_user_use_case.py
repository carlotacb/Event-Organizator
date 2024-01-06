from datetime import date

from app.events.domain.exceptions import MissingParametersToCreateUser
from app.users.application.requests import CreateUserRequest
from app.users.domain.models.user import UserRoles
from app.users.domain.usecases.create_user_use_case import CreateUserUseCase
from tests.api_tests import ApiTests


class TestCreateUserUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository.clear()

    def test__given_create_user_request__when_create_user__then_the_user_is_created(
        self,
    ) -> None:
        # Given
        user_data = CreateUserRequest(
            email="carlota@hackupc.com",
            password="1234",
            first_name="Carlota",
            last_name="Catot",
            username="carlota",
            bio="I'm a cat",
            profile_image="https://www.hacknights.dev/images/hacknight.png",
            study=False,
            work=False,
            date_of_birth="07/05/1996"
        )

        # When
        CreateUserUseCase().execute(user_data)

        # Then
        users = self.user_repository.get_all()
        self.assertEqual(len(users), 1)

    def test__given_create_user_request__when_create_user__then_the_user_have_participant_role(
        self,
    ) -> None:
        # Given
        user_data = CreateUserRequest(
            email="carlota@hackupc.com",
            password="1234",
            first_name="Carlota",
            last_name="Catot",
            username="carlota",
            bio="I'm a cat",
            profile_image="https://www.hacknights.dev/images/hacknight.png",
            study=False,
            work=False,
            date_of_birth="07/05/1996"
        )

        # When
        CreateUserUseCase().execute(user_data)

        # Then
        users = self.user_repository.get_all()
        self.assertEqual(users[0].role, UserRoles.PARTICIPANT)

    def test__given_create_user_with_username_in_uppercase__when_create_user__then_the_username_is_lowercased(
        self,
    ) -> None:
        # Given
        user_data = CreateUserRequest(
            email="carlota@hackupc.com",
            password="1234",
            first_name="Carlota",
            last_name="Catot",
            username="CarLota",
            bio="I'm a cat",
            profile_image="https://www.hacknights.dev/images/hacknight.png",
            study=False,
            work=False,
            date_of_birth="07/05/1996"
        )

        # When
        CreateUserUseCase().execute(user_data)

        # Then
        users = self.user_repository.get_all()
        self.assertEqual(users[0].username, "carlota")

    def test__given_create_user_with_study_true_if_university_is_not_defined__when_create_user__then_MissingParametersToCreateUser_exception_is_raised(
        self,
    ) -> None:
        # Given
        user_data = CreateUserRequest(
            email="carlota@hackupc.com",
            password="1234",
            first_name="Carlota",
            last_name="Catot",
            username="CarLota",
            bio="I'm a cat",
            profile_image="https://www.hacknights.dev/images/hacknight.png",
            study=True,
            work=False,
            date_of_birth="07/05/1996"
        )

        # When / Then
        with self.assertRaises(MissingParametersToCreateUser):
            CreateUserUseCase().execute(user_data)

    def test__given_create_user_with_study_true_if_degree_is_not_defined__when_create_user__then_MissingParametersToCreateUser_exception_is_raised(
        self,
    ) -> None:
        # Given
        user_data = CreateUserRequest(
            email="carlota@hackupc.com",
            password="1234",
            first_name="Carlota",
            last_name="Catot",
            username="CarLota",
            bio="I'm a cat",
            profile_image="https://www.hacknights.dev/images/hacknight.png",
            study=True,
            work=False,
            date_of_birth="07/05/1996",
            university="Universitat Politècnica de Catalunya"
        )

        # When / Then
        with self.assertRaises(MissingParametersToCreateUser):
            CreateUserUseCase().execute(user_data)

    def test__given_create_user_with_study_true_if_expected_graduation_is_not_defined__when_create_user__then_MissingParametersToCreateUser_exception_is_raised(
        self,
    ) -> None:
        # Given
        user_data = CreateUserRequest(
            email="carlota@hackupc.com",
            password="1234",
            first_name="Carlota",
            last_name="Catot",
            username="CarLota",
            bio="I'm a cat",
            profile_image="https://www.hacknights.dev/images/hacknight.png",
            study=True,
            work=False,
            date_of_birth="07/05/1996",
            university="Universitat Politècnica de Catalunya",
            degree="Computer Science"
        )

        # When / Then
        with self.assertRaises(MissingParametersToCreateUser):
            CreateUserUseCase().execute(user_data)

    def test__given_create_user_with_work_true_if_current_job_role_is_not_defined__when_create_user__then_MissingParametersToCreateUser_exception_is_raised(
        self,
    ) -> None:
        # Given
        user_data = CreateUserRequest(
            email="carlota@hackupc.com",
            password="1234",
            first_name="Carlota",
            last_name="Catot",
            username="CarLota",
            bio="I'm a cat",
            profile_image="https://www.hacknights.dev/images/hacknight.png",
            study=False,
            work=True,
            date_of_birth="07/05/1996",
        )

        # When / Then
        with self.assertRaises(MissingParametersToCreateUser):
            CreateUserUseCase().execute(user_data)