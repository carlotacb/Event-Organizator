import uuid

from django.db import IntegrityError

from app.events.infrastructure.persistence.models.orm_event import ORMEvent
from app.questions.domain.exceptions import QuestionDoesNotExist
from app.questions.domain.models.question import Question, QuestionType
from app.questions.domain.repositories import QuestionRepository
from app.questions.infrastructure.persistence.model.orm_question import ORMQuestion


class ORMQuestionRepository(QuestionRepository):

    def update(self, question: Question) -> None:
        try:
            orm_question = ORMQuestion.objects.get(id=question.id)
            orm_question.question = question.question
            orm_question.question_type = question.question_type.name
            orm_question.options = question.options
            orm_question.updated_at = question.updated_at
            orm_question.save()
        except ORMQuestion.DoesNotExist:
            raise QuestionDoesNotExist

    def create(self, question: Question) -> None:
        event = ORMEvent.objects.get(id=question.event.id)

        ORMQuestion(
            id=question.id,
            question=question.question,
            question_type=question.question_type.name,
            options=question.options,
            event=event,
            created_at=question.created_at,
            updated_at=question.updated_at,
        ).save()

    def get(self, question_id: uuid.UUID) -> Question:
        try:
            orm_question = ORMQuestion.objects.get(id=question_id)
            return Question(
                id=orm_question.id,
                question=orm_question.question,
                question_type=QuestionType[orm_question.question_type],
                options=orm_question.options,
                event=orm_question.event,
                created_at=orm_question.created_at,
                updated_at=orm_question.updated_at,
            )
        except ORMQuestion.DoesNotExist:
            raise QuestionDoesNotExist
