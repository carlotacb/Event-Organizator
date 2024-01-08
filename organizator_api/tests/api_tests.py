import uuid
from typing import Optional
from unittest import mock

from django.test import TestCase

from app.events.domain.models.event import Event
from app.events.domain.repositories import EventRepository
from app.events.infrastructure.repository_factories import EventRepositoryFactory
from app.users.domain.models.user import User
from app.users.domain.repositories import UserRepository
from app.users.infrastructure.repository_factories import UserRepositoryFactory
from tests.applications.mocks.application_repository_mock import ApplicationRepositoryMock
from tests.events.domain.EventFactory import EventFactory
from tests.events.mocks.event_repository_mock import EventRepositoryMock
from tests.users.domain.UserFactory import UserFactory
from tests.users.mocks.user_repository_mock import UserRepositoryMock


class ApiTests(TestCase):
    def setUp(self) -> None:
        super().setUp()

        # Events
        self.event_repository = EventRepositoryMock()
        self.event_repository_patcher = mock.patch(
            "app.events.infrastructure.repository_factories.EventRepositoryFactory.create",
            return_value=self.event_repository,
        )
        self.event_repository_patcher.start()

        # Users
        self.user_repository = UserRepositoryMock()
        self.user_repository_patcher = mock.patch(
            "app.users.infrastructure.repository_factories.UserRepositoryFactory.create",
            return_value=self.user_repository,
        )
        self.user_repository_patcher.start()

        # Applications
        self.application_repository = ApplicationRepositoryMock()
        self.application_repository_patcher = mock.patch(
            "app.applications.infrastructure.repository_factories.ApplicationRepositoryFactory.create",
            return_value=self.application_repository,
        )
        self.application_repository_patcher.start()

    def tearDown(self) -> None:
        super().tearDown()
        self.event_repository_patcher.stop()
        self.user_repository_patcher.stop()
        self.application_repository_patcher.stop()

    def given_user_in_repository(self, new_id: uuid.UUID, email: str, username: str, token: Optional[uuid.UUID] = None) -> User:
        user = UserFactory.create(
            new_id=new_id,
            email=email,
            username=username,
            token=token,
        )

        user_repository: UserRepository = UserRepositoryFactory.create()
        user_repository.create(user=user)

        return user

    def given_event_in_repository(self, new_id: uuid.UUID, name: str) -> Event:
        event = EventFactory.create(
            new_id=new_id,
            name=name,
        )

        event_repository: EventRepository = EventRepositoryFactory.create()
        event_repository.create(event=event)

        return event
