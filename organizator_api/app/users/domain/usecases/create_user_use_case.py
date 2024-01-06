import uuid
from datetime import datetime, timezone, date
import bcrypt

from app.events.domain.exceptions import MissingParametersToCreateUser
from app.users.application.requests import CreateUserRequest
from app.users.domain.models.user import User, UserRoles
from app.users.infrastructure.repository_factories import UserRepositoryFactory


class CreateUserUseCase:
    def __init__(self) -> None:
        self.user_repository = UserRepositoryFactory.create()

    def execute(self, user_data: CreateUserRequest) -> None:
        hashed_password = bcrypt.hashpw(
            user_data.password.encode("utf-8"), bcrypt.gensalt()
        )

        if user_data.work and user_data.current_job_role is None:
            raise MissingParametersToCreateUser

        if user_data.study and (user_data.university is None or user_data.degree is None or user_data.expected_graduation is None):
            raise MissingParametersToCreateUser

        user = User(
            id=uuid.uuid4(),
            email=user_data.email,
            password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            username=user_data.username.lower(),
            bio=user_data.bio,
            profile_image=user_data.profile_image,
            date_of_birth=datetime.strptime(user_data.date_of_birth, "%d/%m/%Y"),
            study=user_data.study,
            work=user_data.work,
            university=user_data.university if user_data.university else None,
            degree=user_data.degree if user_data.degree else None,
            expected_graduation=user_data.expected_graduation
            if user_data.expected_graduation
            else None,
            current_job_role=user_data.current_job_role
            if user_data.current_job_role
            else None,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
            role=UserRoles.PARTICIPANT,
        )

        self.user_repository.create(user)
