import uuid
from typing import List, Optional

from django.db import IntegrityError

from app.users.domain.exceptions import UserAlreadyExists, UserNotFound, UserNotLoggedIn
from app.users.domain.models.user import User, UserRoles, TShirtSizes, GenderOptions
from app.users.domain.repositories import UserRepository
from app.users.infrastructure.persistence.models.orm_user import ORMUser


class ORMUserRepository(UserRepository):
    def create(self, user: User) -> None:
        try:
            self._to_model(user).save()
        except IntegrityError:
            raise UserAlreadyExists()

    def get_all(self) -> List[User]:
        return [
            self._to_domain(user) for user in ORMUser.objects.all().order_by("username")
        ]

    def get_by_id(self, user_id: uuid.UUID) -> User:
        try:
            user = self._to_domain(ORMUser.objects.get(id=user_id))
            return user
        except ORMUser.DoesNotExist:
            raise UserNotFound()

    def get_by_token(self, token: Optional[uuid.UUID]) -> User:
        if token is None:
            raise UserNotLoggedIn()
        try:
            user = self._to_domain(ORMUser.objects.get(token=str(token)))
            return user
        except ORMUser.DoesNotExist:
            raise UserNotFound()

    def get_by_username(self, username: str) -> User:
        try:
            user = self._to_domain(ORMUser.objects.get(username=username))
            return user
        except ORMUser.DoesNotExist:
            raise UserNotFound()

    def update(self, user: User) -> None:
        try:
            orm_user = ORMUser.objects.get(id=user.id)
            orm_user.first_name = user.first_name
            orm_user.last_name = user.last_name
            orm_user.username = user.username
            orm_user.bio = user.bio
            orm_user.profile_image = user.profile_image
            orm_user.role = UserRoles(user.role).name
            orm_user.updated_at = user.updated_at
            orm_user.date_of_birth = user.date_of_birth
            orm_user.study = user.study
            orm_user.work = user.work
            orm_user.university = user.university
            orm_user.degree = user.degree
            orm_user.expected_graduation = user.expected_graduation
            orm_user.current_job_role = user.current_job_role
            orm_user.tshirt = TShirtSizes(user.tshirt).name if user.tshirt else None
            orm_user.gender = GenderOptions(user.gender).name if user.gender else None
            orm_user.alimentary_restrictions = user.alimentary_restrictions
            orm_user.github = user.github
            orm_user.linkedin = user.linkedin
            orm_user.devpost = user.devpost
            orm_user.webpage = user.webpage
            orm_user.token = user.token

            orm_user.save()
        except ORMUser.DoesNotExist:
            raise UserNotFound()
        except IntegrityError:
            raise UserAlreadyExists()

    def _to_model(self, user: User) -> ORMUser:
        return ORMUser(
            id=user.id,
            email=user.email,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            bio=user.bio,
            token=user.token,
            profile_image=user.profile_image,
            created_at=user.created_at,
            updated_at=user.updated_at,
            role=user.role.name,
            tshirt=user.tshirt.name if user.tshirt else None,
            alimentary_restrictions=user.alimentary_restrictions,
            date_of_birth=user.date_of_birth,
            study=user.study,
            work=user.work,
            gender=user.gender.name if user.gender else None,
            github=user.github,
            linkedin=user.linkedin,
            devpost=user.devpost,
            webpage=user.webpage,
            university=user.university,
            degree=user.degree,
            expected_graduation=user.expected_graduation,
            current_job_role=user.current_job_role,
        )

    def _to_domain(self, user: ORMUser) -> User:
        return User(
            id=user.id,
            email=user.email,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            bio=user.bio,
            profile_image=user.profile_image,
            token=user.token,
            created_at=user.created_at,
            updated_at=user.updated_at,
            role=UserRoles[user.role],
            tshirt=TShirtSizes[user.tshirt] if user.tshirt else None,
            alimentary_restrictions=user.alimentary_restrictions,
            date_of_birth=user.date_of_birth,
            study=user.study,
            work=user.work,
            gender=GenderOptions[user.gender] if user.gender else None,
            github=user.github,
            linkedin=user.linkedin,
            devpost=user.devpost,
            webpage=user.webpage,
            university=user.university,
            degree=user.degree,
            expected_graduation=user.expected_graduation,
            current_job_role=user.current_job_role,
        )
