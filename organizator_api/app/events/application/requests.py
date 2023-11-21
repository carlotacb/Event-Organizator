from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateEventRequest:
    name: str
    url: str
    description: str
    start_date: datetime
    end_date: datetime
    location: str
    header_image: str
