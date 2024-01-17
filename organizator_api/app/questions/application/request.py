import uuid
from dataclasses import dataclass
from typing import Optional

from app.questions.domain.models.question import QuestionType


@dataclass
class CreateQuestionRequest:
    question: str
    question_type: str
    options: str
    event_id: uuid.UUID


@dataclass
class UpdateQuestionRequest:
    question: Optional[str]
    question_type: Optional[str] = None
    options: Optional[str] = None
