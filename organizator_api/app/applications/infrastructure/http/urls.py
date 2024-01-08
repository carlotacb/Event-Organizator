from django.urls import path

from app.applications.infrastructure.http.views import create_new_application

urlpatterns = [
    path("new", create_new_application),
]
