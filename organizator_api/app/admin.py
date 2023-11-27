from django.contrib import admin

from app.events.infrastructure.persistence.models.orm_event import ORMEvent as Event

admin.site.register(Event)
