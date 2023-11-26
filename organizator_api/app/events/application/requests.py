from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CreateEventRequest:
    name: str
    url: str
    description: str
    start_date: datetime
    end_date: datetime
    location: str
    header_image: str


@dataclass
class UpdateEventRequest:
    name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    header_image: Optional[str] = None
