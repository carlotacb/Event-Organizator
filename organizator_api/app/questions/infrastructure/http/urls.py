from django.urls import path

from app.questions.infrastructure.http.views import create_new_question

urlpatterns = [
    path("new", create_new_question),
]
