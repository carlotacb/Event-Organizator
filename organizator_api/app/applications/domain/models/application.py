import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from app.events.domain.models.event import Event
from app.users.domain.models.user import User


class ApplicationStatus(Enum):
    PENDING = "Under review"
    INVITED = "Invited"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    INVALID = "Invalid"
    REJECTED = "Rejected"
    WAIT_LIST = "Wait list"

    @classmethod
    def choices(cls) -> tuple[tuple[str, str], ...]:
        return tuple((i.name, i.value) for i in cls)


@dataclass
class Application:
    id: uuid.UUID
    user: User
    event: Event
    status: ApplicationStatus
    created_at: datetime
    updated_at: datetime
