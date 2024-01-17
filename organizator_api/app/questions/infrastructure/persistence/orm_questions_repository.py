from typing import List

from django.db import IntegrityError

from app.events.domain.models.event import Event
from app.events.infrastructure.persistence.models.orm_event import ORMEvent
from app.questions.domain.exceptions import QuestionAlreadyExists
from app.questions.domain.models.question import Question, QuestionType
from app.questions.domain.repositories import QuestionRepository
from app.questions.infrastructure.persistence.model.orm_question import ORMQuestion


class ORMQuestionRepository(QuestionRepository):
    def get_all(self) -> List[Question]:
        return [
            self._to_domain(question) for question in ORMQuestion.objects.all()
        ]

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

    def _to_domain(self, question: ORMQuestion) -> Question:
        return Question(
            id=question.id,
            question=question.question,
            question_type=QuestionType[question.question_type],
            options=question.options,
            event=Event(
                id=question.event.id,
                name=question.event.name,
                url=question.event.url,
                description=question.event.description,
                start_date=question.event.start_date,
                end_date=question.event.end_date,
                location=question.event.location,
                header_image=question.event.header_image,
                created_at=question.event.created_at,
                updated_at=question.event.updated_at,
                open_for_participants=question.event.open_for_participants,
                max_participants=question.event.max_participants,
                expected_attrition_rate=question.event.expected_attrition_rate,
                students_only=question.event.students_only,
                age_restrictions=question.event.age_restrictions,
                deleted_at=question.event.deleted_at,
            ),
            created_at=question.created_at,
            updated_at=question.updated_at,
        )