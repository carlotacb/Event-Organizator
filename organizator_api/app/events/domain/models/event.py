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
