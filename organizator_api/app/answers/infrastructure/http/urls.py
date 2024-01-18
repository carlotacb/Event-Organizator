from django.urls import path

from app.answers.infrastructure.http.views import create_new_answer

urlpatterns = [
    path("new", create_new_answer),
]