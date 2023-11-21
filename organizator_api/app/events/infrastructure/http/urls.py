from django.urls import path

from app.events.infrastructure.http.views import create_new_event

urlpatterns = [path("/events", create_new_event)]
