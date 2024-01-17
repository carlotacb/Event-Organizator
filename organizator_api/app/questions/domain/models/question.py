import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from app.events.domain.models.event import Event


class QuestionType(Enum):
    OPTIONS = "Options"
    TEXT = "Text"
    NUMBER = "Number"
    DATE = "Date"

    @classmethod
    def choices(cls) -> tuple[tuple[str, str], ...]:
        return tuple((i.name, i.value) for i in cls)


@dataclass
class Question:
    id: uuid.UUID
    question: str
    question_type: QuestionType
    options: str
    event: Event
    created_at: datetime
    updated_at: datetime
