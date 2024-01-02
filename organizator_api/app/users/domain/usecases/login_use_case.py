import uuid
import bcrypt

from app.users.domain.exceptions import InvalidPassword
from app.users.infrastructure.repository_factories import UserRepositoryFactory


class LoginUseCase:
    def __init__(self) -> None:
        self.user_repository = UserRepositoryFactory.create()

    def execute(self, username: str, password: str) -> uuid.UUID:
        user = self.user_repository.get_by_username(username)
        if user.token is not None:
            return user.token

        if bcrypt.checkpw(password.encode("utf-8"), user.password) is False:
            raise InvalidPassword

        user.token = uuid.uuid4()
        self.user_repository.update(user)

        return user.token
