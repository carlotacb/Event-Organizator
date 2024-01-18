import uuid
from dataclasses import dataclass


@dataclass
class CreateAnswerRequest:
    answer: str
    question_id: uuid.UUID
    application_id: uuid.UUID
