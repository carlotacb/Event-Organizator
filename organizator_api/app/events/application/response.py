from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.events.domain.models.event import Event
from app.events.domain.models.event_applications import EventApplication


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
    open_for_participants: bool
    max_participants: int
    expected_attrition_rate: float
    students_only: bool
    age_restrictions: int

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
            open_for_participants=event.open_for_participants,
            max_participants=event.max_participants,
            expected_attrition_rate=event.expected_attrition_rate,
            students_only=event.students_only,
            age_restrictions=event.age_restrictions,
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
            "open_for_participants": self.open_for_participants,
            "max_participants": self.max_participants,
            "expected_attrition_rate": self.expected_attrition_rate,
            "students_only": self.students_only,
            "age_restrictions": self.age_restrictions,
        }


@dataclass
class EventApplicationResponse:
    name: str
    actual_participants_count: int
    max_participants: int
    expected_attrition_rate: float

    @staticmethod
    def from_event_application(event_application: EventApplication) -> "EventApplicationResponse":
        return EventApplicationResponse(
            name=event_application.name,
            actual_participants_count=event_application.actual_participants_count,
            max_participants=event_application.max_participants,
            expected_attrition_rate=event_application.expected_attrition_rate,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "actual_participants_count": self.actual_participants_count,
            "max_participants": self.max_participants,
            "expected_attrition_rate": self.expected_attrition_rate,
        }