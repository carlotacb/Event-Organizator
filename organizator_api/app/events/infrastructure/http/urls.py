from django.urls import path

from app.events.infrastructure.http.views import (
    create_new_event,
    get_all_events,
    get_all_upcoming_events,
    get_event,
    update_event,
    delete_event,
    get_upcoming_events_with_application_information,
)

urlpatterns = [
    path("new", create_new_event),
    path("", get_all_events),
    path("upcoming", get_all_upcoming_events),
    path("upcoming/applications", get_upcoming_events_with_application_information),
    path("<uuid:event_id>", get_event),
    path("update/<uuid:event_id>", update_event),
    path("delete/<uuid:event_id>", delete_event),
]
