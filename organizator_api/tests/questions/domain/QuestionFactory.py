import uuid
from datetime import datetime

from app.events.domain.models.event import Event
from app.questions.domain.models.question import Question, QuestionType
from tests.events.domain.EventFactory import EventFactory


class QuestionFactory:
    @staticmethod
    def create(
        new_id: uuid.UUID = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
        question: str = "Question",
        question_type: QuestionType = QuestionType.TEXT,
        event: Event = EventFactory().create(),
        options: str = "",
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
    ) -> Question:
        return Question(
            id=new_id,
            question=question,
            question_type=question_type,
            event=event,
            options=options,
            created_at=created_at,
            updated_at=updated_at,
        )
