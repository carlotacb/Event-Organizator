from dataclasses import dataclass


@dataclass
class EventApplication:
    name: str
    actual_participants_count: int
    max_participants: int
    expected_attrition_rate: float
