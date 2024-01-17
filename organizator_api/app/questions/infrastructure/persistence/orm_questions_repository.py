from django.db import IntegrityError

from app.events.infrastructure.persistence.models.orm_event import ORMEvent
from app.questions.domain.exceptions import QuestionAlreadyExists
from app.questions.domain.models.question import Question
from app.questions.domain.repositories import QuestionRepository
from app.questions.infrastructure.persistence.model.orm_question import ORMQuestion


class ORMQuestionRepository(QuestionRepository):
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
