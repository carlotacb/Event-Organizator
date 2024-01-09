import uuid
from datetime import datetime
from typing import Optional

from app.applications.domain.models.application import Application
from app.events.domain.models.event import Event
from app.users.domain.models.user import User
from tests.events.domain.EventFactory import EventFactory
from tests.users.domain.UserFactory import UserFactory


class ApplicationFactory:
    @staticmethod
    def create(
        new_id: uuid.UUID = uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"),
        user: User = UserFactory().create(),
        event: Event = EventFactory().create(),
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
    ) -> Application:
        return Application(
            id=new_id,
            user=user,
            event=event,
            created_at=created_at,
            updated_at=updated_at,
        )
