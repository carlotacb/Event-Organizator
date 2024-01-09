from django.urls import path

from app.applications.infrastructure.http.views import (
    create_new_application,
    get_applications_by_token,
    get_applications_by_event,
)

urlpatterns = [
    path("new", create_new_application),
    path("myevents", get_applications_by_token),
    path("participants/<uuid:event_id>", get_applications_by_event),
]
