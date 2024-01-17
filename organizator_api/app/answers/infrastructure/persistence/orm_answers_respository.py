from django.db import IntegrityError

from app.answers.domain.exceptions import AnswerAlreadyExists
from app.answers.domain.models.answer import Answer
from app.answers.domain.repositories import AnswersRepository
from app.answers.infrastructure.persistence.model.orm_answers import ORMAnswers
from app.applications.infrastructure.persistence.models.orm_application import (
    ORMEventApplication,
)
from app.questions.infrastructure.persistence.model.orm_question import ORMQuestion


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