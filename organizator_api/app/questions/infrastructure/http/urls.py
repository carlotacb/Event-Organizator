from django.urls import path

from app.questions.infrastructure.http.views import create_new_question, update_question

urlpatterns = [
    path("new", create_new_question),
    path("update/<uuid:question_id>", update_question),
]
