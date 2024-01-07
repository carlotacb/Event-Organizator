from unittest import mock

from django.test import TestCase

from tests.applications.mocks.application_repository_mock import ApplicationRepositoryMock
from tests.events.mocks.event_repository_mock import EventRepositoryMock
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
