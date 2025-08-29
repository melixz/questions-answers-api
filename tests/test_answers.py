import pytest
from fastapi.testclient import TestClient


class TestAnswerCreation:
    """Тесты создания ответов."""

    def test_create_answer_success(
        self, client: TestClient, created_question, sample_answer_data
    ):
        """Тест успешного создания ответа."""
        question_id = created_question["id"]

        response = client.post(
            f"/questions/{question_id}/answers/", json=sample_answer_data
        )

        assert response.status_code == 201
        data = response.json()
        assert data["text"] == sample_answer_data["text"]
        assert data["user_id"] == sample_answer_data["user_id"]
        assert data["question_id"] == question_id
        assert "id" in data
        assert "created_at" in data

    @pytest.mark.parametrize("invalid_question_id", [999, 0, -1])
    def test_create_answer_for_nonexistent_question(
        self, client: TestClient, invalid_question_id, sample_answer_data
    ):
        """Тест создания ответа для несуществующего вопроса."""
        response = client.post(
            f"/questions/{invalid_question_id}/answers/", json=sample_answer_data
        )
        assert response.status_code == 404

    @pytest.mark.parametrize("invalid_text", ["", "   ", "\t\n"])
    def test_create_answer_invalid_text(
        self, client: TestClient, created_question, invalid_text
    ):
        """Тест создания ответа с невалидным текстом."""
        question_id = created_question["id"]
        answer_data = {"user_id": "user123", "text": invalid_text}

        response = client.post(f"/questions/{question_id}/answers/", json=answer_data)
        assert response.status_code == 422

    @pytest.mark.parametrize("invalid_user_id", ["", "   ", "\t\n"])
    def test_create_answer_invalid_user_id(
        self, client: TestClient, created_question, invalid_user_id
    ):
        """Тест создания ответа с невалидным user_id."""
        question_id = created_question["id"]
        answer_data = {"user_id": invalid_user_id, "text": "Валидный текст"}

        response = client.post(f"/questions/{question_id}/answers/", json=answer_data)
        assert response.status_code == 422

    @pytest.mark.parametrize(
        "user_id,answer_text",
        [
            ("alice", "Отличный вопрос!"),
            ("bob", "Я думаю, что это зависит от контекста."),
            ("charlie", "Можете привести пример?"),
        ],
    )
    def test_create_different_answers(
        self, client: TestClient, created_question, user_id, answer_text
    ):
        """Тест создания различных ответов."""
        question_id = created_question["id"]
        answer_data = {"user_id": user_id, "text": answer_text}

        response = client.post(f"/questions/{question_id}/answers/", json=answer_data)

        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == user_id
        assert data["text"] == answer_text


class TestAnswerRetrieval:
    """Тесты получения ответов."""

    def test_get_answer_by_id_success(self, client: TestClient, created_answer):
        """Тест успешного получения ответа по ID."""
        answer_id = created_answer["id"]

        response = client.get(f"/answers/{answer_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == answer_id
        assert data["text"] == created_answer["text"]
        assert data["user_id"] == created_answer["user_id"]
        assert data["question_id"] == created_answer["question_id"]

    @pytest.mark.parametrize("invalid_id", [999, 0, -1])
    def test_get_answer_by_invalid_id(self, client: TestClient, invalid_id):
        """Тест получения ответа с невалидным ID."""
        response = client.get(f"/answers/{invalid_id}")
        assert response.status_code == 404

    def test_get_question_with_multiple_answers(
        self, client: TestClient, question_with_answers
    ):
        """Тест получения вопроса с несколькими ответами."""
        question_id = question_with_answers["question"]["id"]
        expected_answers = question_with_answers["answers"]

        response = client.get(f"/questions/{question_id}")

        assert response.status_code == 200
        data = response.json()
        assert len(data["answers"]) == len(expected_answers)

        returned_answer_ids = {answer["id"] for answer in data["answers"]}
        expected_answer_ids = {answer["id"] for answer in expected_answers}
        assert returned_answer_ids == expected_answer_ids


class TestAnswerUpdate:
    """Тесты обновления ответов."""

    def test_update_answer_success(self, client: TestClient, created_answer):
        """Тест успешного обновления ответа."""
        answer_id = created_answer["id"]
        new_text = "Обновленный текст ответа"

        response = client.put(f"/answers/{answer_id}", json={"text": new_text})

        assert response.status_code == 200
        data = response.json()
        assert data["text"] == new_text
        assert data["id"] == answer_id
        assert (
            data["user_id"] == created_answer["user_id"]
        )  # user_id не должен измениться

    @pytest.mark.parametrize("invalid_text", ["", "   ", "\t\n"])
    def test_update_answer_invalid_text(
        self, client: TestClient, created_answer, invalid_text
    ):
        """Тест обновления ответа с невалидным текстом."""
        answer_id = created_answer["id"]

        response = client.put(f"/answers/{answer_id}", json={"text": invalid_text})
        assert response.status_code == 422

    def test_update_nonexistent_answer(self, client: TestClient):
        """Тест обновления несуществующего ответа."""
        response = client.put("/answers/999", json={"text": "Новый текст"})
        assert response.status_code == 404

    def test_update_answer_partial(self, client: TestClient, created_answer):
        """Тест частичного обновления ответа (только текст)."""
        answer_id = created_answer["id"]
        original_user_id = created_answer["user_id"]
        new_text = "Частично обновленный текст"

        response = client.put(f"/answers/{answer_id}", json={"text": new_text})

        assert response.status_code == 200
        data = response.json()
        assert data["text"] == new_text
        assert data["user_id"] == original_user_id  # user_id остается прежним


class TestAnswerDeletion:
    """Тесты удаления ответов."""

    def test_delete_answer_success(self, client: TestClient, created_answer):
        """Тест успешного удаления ответа."""
        answer_id = created_answer["id"]

        delete_response = client.delete(f"/answers/{answer_id}")
        assert delete_response.status_code == 204

        get_response = client.get(f"/answers/{answer_id}")
        assert get_response.status_code == 404

    @pytest.mark.parametrize("invalid_id", [999, 0, -1])
    def test_delete_nonexistent_answer(self, client: TestClient, invalid_id):
        """Тест удаления несуществующего ответа."""
        response = client.delete(f"/answers/{invalid_id}")
        assert response.status_code == 404

    def test_delete_answer_question_remains(self, client: TestClient, created_answer):
        """Тест того, что при удалении ответа вопрос остается."""
        answer_id = created_answer["id"]
        question_id = created_answer["question_id"]

        delete_response = client.delete(f"/answers/{answer_id}")
        assert delete_response.status_code == 204

        get_question_response = client.get(f"/questions/{question_id}")
        assert get_question_response.status_code == 200

        question_data = get_question_response.json()
        assert len(question_data["answers"]) == 0


class TestAnswerIntegration:
    """Интеграционные тесты для ответов."""

    def test_multiple_users_answering_same_question(
        self, client: TestClient, created_question
    ):
        """Тест создания ответов от разных пользователей на один вопрос."""
        question_id = created_question["id"]
        users_and_answers = [
            ("alice", "Первый ответ от Alice"),
            ("bob", "Второй ответ от Bob"),
            ("charlie", "Третий ответ от Charlie"),
        ]

        created_answers = []
        for user_id, text in users_and_answers:
            answer_data = {"user_id": user_id, "text": text}
            response = client.post(
                f"/questions/{question_id}/answers/", json=answer_data
            )
            assert response.status_code == 201
            created_answers.append(response.json())

        question_response = client.get(f"/questions/{question_id}")
        assert question_response.status_code == 200
        question_data = question_response.json()
        assert len(question_data["answers"]) == len(users_and_answers)

    def test_answer_lifecycle(
        self, client: TestClient, created_question, sample_answer_data
    ):
        """Тест полного жизненного цикла ответа: создание -> получение -> обновление -> удаление."""
        question_id = created_question["id"]

        create_response = client.post(
            f"/questions/{question_id}/answers/", json=sample_answer_data
        )
        assert create_response.status_code == 201
        answer_id = create_response.json()["id"]

        get_response = client.get(f"/answers/{answer_id}")
        assert get_response.status_code == 200

        new_text = "Обновленный текст в жизненном цикле"
        update_response = client.put(f"/answers/{answer_id}", json={"text": new_text})
        assert update_response.status_code == 200
        assert update_response.json()["text"] == new_text

        delete_response = client.delete(f"/answers/{answer_id}")
        assert delete_response.status_code == 204

        final_get_response = client.get(f"/answers/{answer_id}")
        assert final_get_response.status_code == 404
