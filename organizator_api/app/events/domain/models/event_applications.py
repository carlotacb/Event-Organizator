import uuid
from dataclasses import dataclass


@dataclass
class EventApplication:
    event_id: uuid.UUID
    name: str
    actual_participants_count: int
    max_participants: int
    expected_attrition_rate: float
