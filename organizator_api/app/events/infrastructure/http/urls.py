from django.urls import path

from app.events.infrastructure.http.views import (
    create_new_event,
    get_all_events,
    get_event,
)

urlpatterns = [
    path("new", create_new_event),
    path("", get_all_events),
    path("<uuid:event_id>", get_event),
]
