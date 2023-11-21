from unittest import mock

from django.test import TestCase

from tests.events.mocks.event_repository_mock import EventRepositoryMock


class ApiTests(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.event_repository = EventRepositoryMock()
        self.event_repository_patcher = mock.patch(
            "app.events.infrastructure.repository_factories.EventRepositoryFactory.create",
            return_value=self.event_repository,
        )
        self.event_repository_patcher.start()


    def tearDown(self) -> None:
        super().tearDown()
        self.event_repository_patcher.stop()