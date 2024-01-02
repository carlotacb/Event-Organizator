import uuid
from datetime import datetime, timezone
import bcrypt

from app.users.application.requests import CreateUserRequest
from app.users.domain.models.user import User
from app.users.infrastructure.repository_factories import UserRepositoryFactory


class CreateUserUseCase:
    def __init__(self) -> None:
        self.user_repository = UserRepositoryFactory.create()

    def execute(self, user_data: CreateUserRequest) -> None:
        hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())

        user = User(
            id=uuid.uuid4(),
            email=user_data.email,
            password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            username=user_data.username,
            bio=user_data.bio,
            profile_image=user_data.profile_image,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        )

        self.user_repository.create(user)
