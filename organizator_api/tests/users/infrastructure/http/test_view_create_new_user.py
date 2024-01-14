import json
from datetime import datetime

from app.users.domain.models.user import UserRoles
from tests.api_tests import ApiTests


class TestViewCreateNewUser(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository.clear()

    def test__given_unexpected_body__when_create_user__then_unexpected_body_is_returned(
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
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.content, b"Unexpected body")

    def test__given_a_uncompleted_body__when_create_user__then_unexpected_body_is_returned(
        self,
    ) -> None:
        # Given
        body = {
            "email": "carlota@hackpc.com",
            "password": "12345678",
            "first_name": "Carlota",
            "last_name": "Catot",
        }

        # When
        response = self.client.post(
            "/organizator-api/users/new",
            json.dumps(body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.content, b"Unexpected body")

    def test__given_user_body_that_study_but_have_no_study_information__when_create_user__then_missing_study_information_is_returned(
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
            "date_of_birth": "07/05/1996",
            "study": True,
        }

        # When
        response = self.client.post(
            "/organizator-api/users/new",
            json.dumps(body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.content, b"Missing study information to create user")

    def test__given_user_body_that_work_but_have_no_work_information__when_create_user__then_missing_work_information_is_returned(
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
            "date_of_birth": "07/05/1996",
            "work": True,
        }

        # When
        response = self.client.post(
            "/organizator-api/users/new",
            json.dumps(body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.content, b"Missing work information to create user")

    def test__given_user_already_exists__when_create_user__then_user_already_exists_is_returned(
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
            "date_of_birth": "07/05/1996",
            "study": True,
            "university": "UPC",
            "degree": "Computer Science",
            "expected_graduation": "07/05/2025",
        }
        body2 = {
            "email": "carkbra@hackupc.com",
            "password": "12345678",
            "first_name": "Carlota",
            "last_name": "Catot",
            "username": "carlota",
            "bio": "I'm Carlota",
            "profile_image": "https://www.google.com",
            "date_of_birth": "07/05/1996",
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

    def test__given_a_json_body_with_a_student_user__when_create_user__then_the_user_is_created_and_stored_in_db(
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
            "date_of_birth": "07/05/1996",
            "study": True,
            "university": "UPC",
            "degree": "Computer Science",
            "expected_graduation": "07/05/2025",
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
        self.assertEqual(user.first_name, "Carlota")
        self.assertEqual(user.last_name, "Catot")
        self.assertEqual(user.username, "carlota")
        self.assertEqual(user.bio, "I'm Carlota")
        self.assertEqual(user.profile_image, "https://www.google.com")
        self.assertEqual(user.role, UserRoles.PARTICIPANT)
        self.assertEqual(user.study, True)
        self.assertEqual(user.work, False)
        self.assertEqual(user.university, "UPC")
        self.assertEqual(user.degree, "Computer Science")
        self.assertEqual(user.expected_graduation, datetime(2025, 5, 7, 0, 0))
        self.assertEqual(user.current_job_role, None)

    def test__given_a_json_body_with_a_worker_user__when_create_user__then_the_user_is_created_and_stored_in_db(
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
            "date_of_birth": "07/05/1996",
            "work": True,
            "current_job_role": "Software Engineer",
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
        self.assertEqual(user.first_name, "Carlota")
        self.assertEqual(user.last_name, "Catot")
        self.assertEqual(user.username, "carlota")
        self.assertEqual(user.bio, "I'm Carlota")
        self.assertEqual(user.profile_image, "https://www.google.com")
        self.assertEqual(user.role, UserRoles.PARTICIPANT)
        self.assertEqual(user.study, False)
        self.assertEqual(user.work, True)
        self.assertEqual(user.university, None)
        self.assertEqual(user.degree, None)
        self.assertEqual(user.expected_graduation, None)
        self.assertEqual(user.current_job_role, "Software Engineer")

    def test__given_user_body_that_is_not_studying_neither_working__when_create_user__then_the_user_is_created_and_stored_in_db(
        self,
    ) -> None:
        # Given
        body = {
            "email": "carkbra@hackupc.com",
            "password": "12345678",
            "first_name": "Carlota",
            "last_name": "Catot",
            "username": "carlota",
            "bio": "I'm Carlota",
            "profile_image": "https://www.google.com",
            "date_of_birth": "07/05/1996",
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
        self.assertEqual(user.work, False)
        self.assertEqual(user.study, False)
        self.assertEqual(user.university, None)
        self.assertEqual(user.degree, None)
        self.assertEqual(user.expected_graduation, None)
        self.assertEqual(user.current_job_role, None)
