import uuid
from typing import List

from django.db import IntegrityError

from app.answers.domain.exceptions import AnswerAlreadyExists
from app.answers.domain.models.answer import Answer
from app.answers.domain.repositories import AnswersRepository
from app.answers.infrastructure.persistence.model.orm_answers import ORMAnswers
from app.applications.domain.models.application import Application, ApplicationStatus
from app.applications.infrastructure.persistence.models.orm_application import (
    ORMEventApplication,
)
from app.events.domain.models.event import Event
from app.questions.domain.models.question import Question, QuestionType
from app.questions.infrastructure.persistence.model.orm_question import ORMQuestion
from app.users.domain.models.user import User, UserRoles


class ORMAnswersRepository(AnswersRepository):
    def create(self, answer: Answer) -> None:
        question = ORMQuestion.objects.get(id=answer.question.id)
        application = ORMEventApplication.objects.get(id=answer.application.id)

        try:
            ORMAnswers(
                id=answer.id,
                answer=answer.answer,
                question=question,
                application=application,
                created_at=answer.created_at,
                updated_at=answer.updated_at,
            ).save()
        except IntegrityError:
            raise AnswerAlreadyExists

    def get_by_application_id(self, application_id: uuid.UUID) -> List[Answer]:
        return [
            self._to_domain(answer)
            for answer in ORMAnswers.objects.filter(application_id=application_id)
        ]

    def _to_domain(self, answer: ORMAnswers) -> Answer:
        return Answer(
            id=answer.id,
            answer=answer.answer,
            question=Question(
                id=answer.question.id,
                question=answer.question.question,
                question_type=QuestionType[answer.question.question_type],
                options=answer.question.options,
                event=Event(
                    id=answer.question.event.id,
                    name=answer.question.event.name,
                    url=answer.question.event.url,
                    description=answer.question.event.description,
                    start_date=answer.question.event.start_date,
                    end_date=answer.question.event.end_date,
                    location=answer.question.event.location,
                    header_image=answer.question.event.header_image,
                    created_at=answer.question.event.created_at,
                    updated_at=answer.question.event.updated_at,
                    open_for_participants=answer.question.event.open_for_participants,
                    max_participants=answer.question.event.max_participants,
                    expected_attrition_rate=answer.question.event.expected_attrition_rate,
                    students_only=answer.question.event.students_only,
                    age_restrictions=answer.question.event.age_restrictions,
                    deleted_at=answer.question.event.deleted_at,
                ),
                created_at=answer.question.created_at,
                updated_at=answer.question.updated_at,
            ),
            application=Application(
                id=answer.application.id,
                event=Event(
                    id=answer.application.event.id,
                    name=answer.application.event.name,
                    url=answer.application.event.url,
                    description=answer.application.event.description,
                    start_date=answer.application.event.start_date,
                    end_date=answer.application.event.end_date,
                    location=answer.application.event.location,
                    header_image=answer.application.event.header_image,
                    created_at=answer.application.event.created_at,
                    updated_at=answer.application.event.updated_at,
                    open_for_participants=answer.application.event.open_for_participants,
                    max_participants=answer.application.event.max_participants,
                    expected_attrition_rate=answer.application.event.expected_attrition_rate,
                    students_only=answer.application.event.students_only,
                    age_restrictions=answer.application.event.age_restrictions,
                    deleted_at=answer.application.event.deleted_at,
                ),
                user=User(
                    id=answer.application.user.id,
                    email=answer.application.user.email,
                    first_name=answer.application.user.first_name,
                    last_name=answer.application.user.last_name,
                    password=answer.application.user.password,
                    username=answer.application.user.username,
                    bio=answer.application.user.bio,
                    profile_image=answer.application.user.profile_image,
                    role=UserRoles[answer.application.user.role],
                    created_at=answer.application.user.created_at,
                    updated_at=answer.application.user.updated_at,
                    date_of_birth=answer.application.user.date_of_birth,
                    study=answer.application.user.study,
                    work=answer.application.user.work,
                ),
                status=ApplicationStatus[answer.application.status],
                created_at=answer.application.created_at,
                updated_at=answer.application.updated_at,
            ),
            created_at=answer.created_at,
            updated_at=answer.updated_at,
        )
