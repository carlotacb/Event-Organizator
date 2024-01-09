from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CreateEventRequest:
    name: str
    url: str
    description: str
    start_date: str
    end_date: str
    location: str
    header_image: str
    open_for_participants: bool
    max_participants: int
    expected_attrition_rate: float
    students_only: bool
    age_restrictions: int

@dataclass
class UpdateEventRequest:
    name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    location: Optional[str] = None
    header_image: Optional[str] = None
    open_for_participants: Optional[bool] = False
    max_participants: Optional[int] = None
    expected_attrition_rate: Optional[float] = None
    students_only: Optional[bool] = False
    age_restrictions: Optional[int] = None
