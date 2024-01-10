import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Event:
    id: uuid.UUID
    name: str
    url: str
    description: str
    start_date: datetime
    end_date: datetime
    location: str
    header_image: str
    created_at: datetime
    updated_at: datetime
    open_for_participants: bool
    max_participants: int
    expected_attrition_rate: float
    students_only: bool
    age_restrictions: int
    deleted_at: Optional[datetime] = None
