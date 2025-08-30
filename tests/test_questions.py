import pytest
from fastapi.testclient import TestClient


class TestQuestionCreation:
    """Тесты создания вопросов."""

    def test_create_question_success(self, client: TestClient, sample_question_data):
        """Тест успешного создания вопроса."""
        response = client.post("/questions/", json=sample_question_data)

        assert response.status_code == 201
        data = response.json()
        assert data["text"] == sample_question_data["text"]
        assert "id" in data
        assert "created_at" in data

    @pytest.mark.parametrize(
        "invalid_text",
        [
            "",
            "   ",
            "\t\n",
        ],
    )
    def test_create_question_invalid_text(self, client: TestClient, invalid_text):
        """Тест создания вопроса с невалидным текстом."""
        response = client.post("/questions/", json={"text": invalid_text})
        assert response.status_code == 422

    @pytest.mark.parametrize(
        "question_text",
        [
            "Что такое FastAPI?",
            "Как работает SQLAlchemy?",
            "Зачем нужен pytest?",
        ],
    )
    def test_create_different_questions(self, client: TestClient, question_text):
        """Тест создания различных вопросов."""
        response = client.post("/questions/", json={"text": question_text})

        assert response.status_code == 201
        data = response.json()
        assert data["text"] == question_text


class TestQuestionRetrieval:
    """Тесты получения вопросов."""

    def test_get_all_questions_empty(self, client: TestClient):
        """Тест получения пустого списка вопросов."""
        response = client.get("/questions/")

        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_get_all_questions_with_data(self, client: TestClient, multiple_questions):
        """Тест получения списка вопросов с данными."""
        response = client.get("/questions/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == len(multiple_questions)

        created_ids = {q["id"] for q in multiple_questions}
        returned_ids = {q["id"] for q in data}
        assert created_ids == returned_ids

    def test_get_question_by_id_success(self, client: TestClient, created_question):
        """Тест успешного получения вопроса по ID."""
        question_id = created_question["id"]
        response = client.get(f"/questions/{question_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == question_id
        assert data["text"] == created_question["text"]
        assert "answers" in data

    @pytest.mark.parametrize("invalid_id", [999, 0, -1])
    def test_get_question_by_invalid_id(self, client: TestClient, invalid_id):
        """Тест получения вопроса с невалидным ID."""
        response = client.get(f"/questions/{invalid_id}")
        assert response.status_code == 404

    def test_get_question_with_answers(self, client: TestClient, question_with_answers):
        """Тест получения вопроса с ответами."""
        question_id = question_with_answers["question"]["id"]
        response = client.get(f"/questions/{question_id}")

        assert response.status_code == 200
        data = response.json()
        assert len(data["answers"]) == len(question_with_answers["answers"])


class TestQuestionDeletion:
    """Тесты удаления вопросов."""

    def test_delete_question_success(self, client: TestClient, created_question):
        """Тест успешного удаления вопроса."""
        question_id = created_question["id"]

        delete_response = client.delete(f"/questions/{question_id}")
        assert delete_response.status_code == 204

        get_response = client.get(f"/questions/{question_id}")
        assert get_response.status_code == 404

    def test_delete_question_with_answers(
        self, client: TestClient, question_with_answers
    ):
        """Тест удаления вопроса с ответами (каскадное удаление)."""
        question_id = question_with_answers["question"]["id"]
        answer_ids = [answer["id"] for answer in question_with_answers["answers"]]

        delete_response = client.delete(f"/questions/{question_id}")
        assert delete_response.status_code == 204

        get_question_response = client.get(f"/questions/{question_id}")
        assert get_question_response.status_code == 404

        for answer_id in answer_ids:
            get_answer_response = client.get(f"/answers/{answer_id}")
            assert get_answer_response.status_code == 404

    @pytest.mark.parametrize("invalid_id", [999, 0, -1])
    def test_delete_nonexistent_question(self, client: TestClient, invalid_id):
        """Тест удаления несуществующего вопроса."""
        response = client.delete(f"/questions/{invalid_id}")
        assert response.status_code == 404
