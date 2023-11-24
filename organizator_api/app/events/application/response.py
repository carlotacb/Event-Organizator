from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.events.domain.models.event import Event


@dataclass
class EventResponse:
    id: str
    name: str
    url: str
    description: str
    start_date: datetime
    end_date: datetime
    location: str
    header_image: str
    deleted: bool

    @staticmethod
    def from_event(event: Event) -> "EventResponse":
        return EventResponse(
            id=str(event.id),
            name=event.name,
            url=event.url,
            description=event.description,
            start_date=event.start_date,
            end_date=event.end_date,
            location=event.location,
            header_image=event.header_image,
            deleted=event.deleted_at is not None,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "description": self.description,
            "start_date": self.start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end_date": self.end_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "location": self.location,
            "header_image": self.header_image,
            "deleted": self.deleted,
        }
