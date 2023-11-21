import uuid
from datetime import datetime
from typing import Optional

from app.events.domain.models.event import Event


class EventFactory:
    @staticmethod
    def create(
        name: str = "HackUPC 2023",
        description: str = "The biggest student hackathon in Europe",
        url: str = "https://www.hackupc.com/",
        start_date: datetime = datetime.strptime(
            "2023-05-12T16:00:00Z", "%Y-%m-%dT%H:%M:%SZ"
        ),
        end_date: datetime = datetime.strptime(
            "2023-05-14T18:00:00Z", "%Y-%m-%dT%H:%M:%SZ"
        ),
        location: str = "UPC Campus Nord",
        header_image: str = "https://hackupc.com/ogimage.png",
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
        deleted_at: Optional[datetime] = None,
    ) -> Event:
        return Event(
            id=uuid.uuid4(),
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
        )
