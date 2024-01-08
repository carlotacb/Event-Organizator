import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.events.domain.models.event import Event
from app.users.domain.models.user import User


@dataclass
class Application:
    id: uuid.UUID
    user: User
    event: Event
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
