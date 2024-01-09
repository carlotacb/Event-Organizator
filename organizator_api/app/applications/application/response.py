from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.applications.domain.models.application import Application
from app.events.application.response import EventResponse
from app.events.domain.models.event import Event
from app.users.application.response import UserResponse
from app.users.domain.models.user import User


@dataclass
class ApplicationResponse:
    id: str
    user: User
    event: Event
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_application(application: Application) -> "ApplicationResponse":
        return ApplicationResponse(
            id=str(application.id),
            user=application.user,
            event=application.event,
            created_at=application.created_at,
            updated_at=application.updated_at,
        )

    def to_dict_without_user(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "event": EventResponse.from_event(self.event).to_dict(),
            "created_at": self.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "updated_at": self.updated_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

    def to_dict_without_event(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "user": UserResponse.from_user(self.user).to_dict(),
            "created_at": self.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "updated_at": self.updated_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
