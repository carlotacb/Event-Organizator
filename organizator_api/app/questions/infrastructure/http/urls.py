from django.urls import path

from app.questions.infrastructure.http.views import (
    create_new_question,
    update_question,
    get_questions_by_event,
)

urlpatterns = [
    path("new", create_new_question),
    path("event/<uuid:event_id>", get_questions_by_event),
    path("update/<uuid:question_id>", update_question),
]
