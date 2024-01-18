import uuid
from datetime import datetime

from app.answers.domain.models.answer import Answer
from app.applications.domain.models.application import Application
from app.questions.domain.models.question import Question
from tests.applications.domain.ApplicationFactory import ApplicationFactory
from tests.questions.domain.QuestionFactory import QuestionFactory


class AnswerFactory:
    @staticmethod
    def create(
        new_id: uuid.UUID = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
        application: Application = ApplicationFactory().create(),
        question: Question = QuestionFactory().create(),
        answer: str = "This is the dummy answer",
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
    ) -> Answer:
        return Answer(
            id=new_id,
            application=application,
            question=question,
            answer=answer,
            created_at=created_at,
            updated_at=updated_at,
        )
