from django.urls import path

from app.events.infrastructure.http.views import create_new_event

urlpatterns = [path("new", create_new_event)]
