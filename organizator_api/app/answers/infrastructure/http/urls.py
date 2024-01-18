from django.urls import path

from app.answers.infrastructure.http.views import (
    create_new_answer,
    get_answers_for_application,
)

urlpatterns = [
    path("new", create_new_answer),
    path("application/<uuid:application_id>", get_answers_for_application),
]
