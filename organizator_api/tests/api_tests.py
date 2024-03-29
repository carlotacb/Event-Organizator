import uuid
from typing import Optional
from unittest import mock

from django.test import TestCase

from app.applications.domain.models.application import Application
from app.applications.infrastructure.persistence.orm_applications_respository import (
    ORMApplicationRepository,
)
from app.events.domain.models.event import Event
from app.events.infrastructure.persistence.orm_event_repository import (
    ORMEventRepository,
)
from app.questions.domain.models.question import Question
from app.questions.infrastructure.persistence.orm_questions_repository import (
    ORMQuestionRepository,
)
from app.users.domain.models.user import User
from app.users.domain.repositories import UserRepository
from app.users.infrastructure.persistence.orm_user_repository import ORMUserRepository
from app.users.infrastructure.repository_factories import UserRepositoryFactory
from tests.answers.mocks.answer_repository_mock import AnswerRepositoryMock
from tests.applications.domain.ApplicationFactory import ApplicationFactory
from tests.applications.mocks.application_repository_mock import (
    ApplicationRepositoryMock,
)
from tests.events.domain.EventFactory import EventFactory
from tests.events.mocks.event_repository_mock import EventRepositoryMock
from tests.questions.domain.QuestionFactory import QuestionFactory
from tests.questions.mocks.question_repository_mock import QuestionRepositoryMock
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

        self.question_repository = QuestionRepositoryMock()
        self.question_repository_patcher = mock.patch(
            "app.questions.infrastructure.repository_factories.QuestionRepositoryFactory.create",
            return_value=self.question_repository,
        )
        self.question_repository_patcher.start()

        self.answer_repository = AnswerRepositoryMock()
        self.answer_repository_patcher = mock.patch(
            "app.answers.infrastructure.repository_factories.AnswerRepositoryFactory.create",
            return_value=self.answer_repository,
        )
        self.answer_repository_patcher.start()

    def tearDown(self) -> None:
        super().tearDown()
        self.event_repository_patcher.stop()
        self.user_repository_patcher.stop()
        self.application_repository_patcher.stop()
        self.question_repository_patcher.stop()
        self.answer_repository_patcher.stop()

    def given_user_in_repository(
        self,
        new_id: uuid.UUID,
        email: str,
        username: str,
        token: Optional[uuid.UUID] = None,
    ) -> User:
        user = UserFactory.create(
            new_id=new_id,
            email=email,
            username=username,
            token=token,
        )

        user_repository: UserRepository = UserRepositoryFactory.create()
        user_repository.create(user=user)

        return user

    def given_user_in_orm(
        self,
        new_id: uuid.UUID,
        email: str,
        username: str,
        token: Optional[uuid.UUID] = None,
    ) -> User:
        user = UserFactory.create(
            new_id=new_id,
            email=email,
            username=username,
            token=token,
        )

        ORMUserRepository().create(user=user)

        return user

    def given_event_in_orm(self, new_id: uuid.UUID, name: str) -> Event:
        event = EventFactory.create(
            new_id=new_id,
            name=name,
        )

        ORMEventRepository().create(event=event)

        return event

    def given_application_in_orm(
        self,
        new_id: uuid.UUID,
    ) -> Application:
        application = ApplicationFactory.create(
            new_id=new_id,
            user=self.given_user_in_orm(
                new_id=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"),
                email="email",
                username="username",
            ),
            event=self.given_event_in_orm(
                new_id=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"), name="event"
            ),
        )

        ORMApplicationRepository().create(application=application)

        return application

    def given_question_in_orm(
        self,
        new_id: uuid.UUID,
    ) -> Question:
        question = QuestionFactory.create(
            new_id=new_id,
            event=self.given_event_in_orm(
                new_id=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"), name="event"
            ),
        )

        ORMQuestionRepository().create(question=question)

        return question
