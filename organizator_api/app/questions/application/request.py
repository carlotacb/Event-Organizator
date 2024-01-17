import uuid
from dataclasses import dataclass

from app.questions.domain.models.question import QuestionType


@dataclass
class CreateQuestionRequest:
    question: str
    question_type: str
    options: str
    event_id: uuid.UUID


@dataclass
class UpdateQuestionRequest:
    question: str
    question_type: str
    options: str
