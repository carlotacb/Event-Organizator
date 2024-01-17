import uuid
from dataclasses import dataclass
from datetime import datetime

from app.applications.domain.models.application import Application
from app.questions.domain.models.question import Question


@dataclass
class Answer:
    id: uuid.UUID
    answer: str
    question: Question
    application: Application
    created_at: datetime
    updated_at: datetime