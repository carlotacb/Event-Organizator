from django.urls import path

from app.applications.infrastructure.http.views import (
    create_new_application,
    get_applications_by_token,
    get_applications_by_event,
    get_application_status,
    update_application_status,
    cancel_application,
    confirm_application,
)

urlpatterns = [
    path("new", create_new_application),
    path("myevents", get_applications_by_token),
    path("update/<uuid:application_id>", update_application_status),
    path("cancel/<uuid:application_id>", cancel_application),
    path("confirm/<uuid:application_id>", confirm_application),
    path("status/<uuid:event_id>", get_application_status),
    path("participants/<uuid:event_id>", get_applications_by_event),
]
