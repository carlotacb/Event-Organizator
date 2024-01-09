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
    deleted_at: Optional[datetime] = None
    open_for_participants: bool = False
    max_participants: Optional[int] = None
    expected_attrition_rate: Optional[float] = None
    students_only: bool = False
    age_restrictions: Optional[int] = None
