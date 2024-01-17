from tests.api_tests import ApiTests


class TestORMAnswerRepositoryCreate(ApiTests):
    def test__given_a_answer_with_a_valid_question_and_user__when_create__then_answer_is_saved(
        self,
    ) -> None:
        # Given
        question = self.given_question_in_orm(
            new_id=uuid.UUID("ef6f6fb3-ba46-43dd-a0da-95de8125b1cc"), name="question"
        )
        answer = Answer(
            id=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"),
            answer="answer",
            question=question,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        )

        # When
        ORMAnswerRepository().create(answer=answer)

        # Then
        self.assertIsNotNone(ORMAnswer.objects.get(id=str(answer.id)))
