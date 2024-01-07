import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Application:
    id: uuid.UUID
    user_id: uuid.UUID
    event_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
