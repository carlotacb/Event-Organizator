import uuid
from datetime import datetime
from typing import Optional

from app.events.domain.models.event import Event


class EventFactory:
    @staticmethod
    def create(
        new_id: uuid.UUID = uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"),
        name: str = "HackUPC 2023",
        description: str = "The biggest student hackathon in Europe",
        url: str = "https://www.hackupc.com/",
        start_date: datetime = datetime(2023, 5, 12, 16, 0),
        end_date: datetime = datetime(2023, 5, 14, 18, 0),
        location: str = "UPC Campus Nord",
        header_image: str = "https://hackupc.com/ogimage.png",
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
        deleted_at: Optional[datetime] = None,
        open_for_participants: bool = True,
        max_participants: int = 100,
        expected_attrition_rate: float = 0.1,
        students_only: bool = True,
        age_restrictions: int = 16,
    ) -> Event:
        return Event(
            id=new_id,
            name=name,
            description=description,
            url=url,
            start_date=start_date,
            end_date=end_date,
            location=location,
            header_image=header_image,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            open_for_participants=open_for_participants,
            max_participants=max_participants,
            expected_attrition_rate=expected_attrition_rate,
            students_only=students_only,
            age_restrictions=age_restrictions,
        )
