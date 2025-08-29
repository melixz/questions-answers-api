import pytest
from fastapi.testclient import TestClient


class TestAPIIntegration:
    """Интеграционные тесты для проверки взаимодействия между компонентами."""

    def test_complete_qa_workflow(self, client: TestClient):
        """Тест полного рабочего процесса: создание вопроса -> добавление ответов -> получение -> обновление -> удаление."""

        question_data = {"text": "Как работает FastAPI?"}
        question_response = client.post("/questions/", json=question_data)
        assert question_response.status_code == 201
        question = question_response.json()
        question_id = question["id"]

        answers_data = [
            {
                "user_id": "expert1",
                "text": "FastAPI - это современный веб-фреймворк для Python",
            },
            {
                "user_id": "expert2",
                "text": "Он основан на стандартных аннотациях типов Python",
            },
            {
                "user_id": "expert3",
                "text": "FastAPI автоматически генерирует документацию API",
            },
        ]

        created_answers = []
        for answer_data in answers_data:
            answer_response = client.post(
                f"/questions/{question_id}/answers/", json=answer_data
            )
            assert answer_response.status_code == 201
            created_answers.append(answer_response.json())

        get_question_response = client.get(f"/questions/{question_id}")
        assert get_question_response.status_code == 200
        question_with_answers = get_question_response.json()
        assert len(question_with_answers["answers"]) == len(answers_data)

        updated_question_text = "Как работает FastAPI и почему он популярен?"
        update_question_response = client.put(
            f"/questions/{question_id}", json={"text": updated_question_text}
        )
        assert update_question_response.status_code == 200
        assert update_question_response.json()["text"] == updated_question_text

        first_answer_id = created_answers[0]["id"]
        updated_answer_text = "FastAPI - это высокопроизводительный веб-фреймворк для Python с автоматической валидацией"
        update_answer_response = client.put(
            f"/answers/{first_answer_id}", json={"text": updated_answer_text}
        )
        assert update_answer_response.status_code == 200
        assert update_answer_response.json()["text"] == updated_answer_text

        second_answer_id = created_answers[1]["id"]
        delete_answer_response = client.delete(f"/answers/{second_answer_id}")
        assert delete_answer_response.status_code == 204

        get_deleted_answer_response = client.get(f"/answers/{second_answer_id}")
        assert get_deleted_answer_response.status_code == 404

        final_question_response = client.get(f"/questions/{question_id}")
        assert final_question_response.status_code == 200
        final_question_data = final_question_response.json()
        assert len(final_question_data["answers"]) == len(answers_data) - 1

        delete_question_response = client.delete(f"/questions/{question_id}")
        assert delete_question_response.status_code == 204

        get_deleted_question_response = client.get(f"/questions/{question_id}")
        assert get_deleted_question_response.status_code == 404

        for answer in created_answers:
            if answer["id"] != second_answer_id:
                get_answer_response = client.get(f"/answers/{answer['id']}")
                assert get_answer_response.status_code == 404

    @pytest.mark.parametrize("num_questions", [1, 5, 10])
    def test_multiple_questions_with_answers(self, client: TestClient, num_questions):
        """Тест создания множественных вопросов с ответами."""
        created_questions = []

        for i in range(num_questions):
            question_data = {"text": f"Вопрос номер {i + 1}"}
            response = client.post("/questions/", json=question_data)
            assert response.status_code == 201
            created_questions.append(response.json())

        for question in created_questions:
            question_id = question["id"]
            for j in range(2):
                answer_data = {
                    "user_id": f"user{j + 1}",
                    "text": f"Ответ {j + 1} на вопрос {question_id}",
                }
                response = client.post(
                    f"/questions/{question_id}/answers/", json=answer_data
                )
                assert response.status_code == 201

        all_questions_response = client.get("/questions/")
        assert all_questions_response.status_code == 200
        all_questions = all_questions_response.json()
        assert len(all_questions) == num_questions

        for question in created_questions:
            question_response = client.get(f"/questions/{question['id']}")
            assert question_response.status_code == 200
            question_data = question_response.json()
            assert len(question_data["answers"]) == 2

    def test_concurrent_answers_to_same_question(
        self, client: TestClient, created_question
    ):
        """Тест добавления ответов от разных пользователей к одному вопросу."""
        question_id = created_question["id"]

        concurrent_answers = [
            {"user_id": "alice", "text": "Ответ от Alice"},
            {"user_id": "bob", "text": "Ответ от Bob"},
            {"user_id": "charlie", "text": "Ответ от Charlie"},
            {"user_id": "diana", "text": "Ответ от Diana"},
            {"user_id": "eve", "text": "Ответ от Eve"},
        ]

        created_answer_ids = []
        for answer_data in concurrent_answers:
            response = client.post(
                f"/questions/{question_id}/answers/", json=answer_data
            )
            assert response.status_code == 201
            created_answer_ids.append(response.json()["id"])

        question_response = client.get(f"/questions/{question_id}")
        assert question_response.status_code == 200
        question_data = question_response.json()
        assert len(question_data["answers"]) == len(concurrent_answers)

        for answer_id in created_answer_ids:
            answer_response = client.get(f"/answers/{answer_id}")
            assert answer_response.status_code == 200
            answer_data = answer_response.json()
            assert answer_data["question_id"] == question_id

    def test_api_error_handling_consistency(self, client: TestClient):
        """Тест консистентности обработки ошибок в API."""

        not_found_endpoints = [
            "/questions/999",
            "/answers/999",
        ]

        for endpoint in not_found_endpoints:
            response = client.get(endpoint)
            assert response.status_code == 404

        bad_request_cases = [
            ("/questions/", {"text": ""}),
            ("/questions/", {"text": "   "}),
        ]

        for endpoint, data in bad_request_cases:
            response = client.post(endpoint, json=data)
            assert response.status_code == 422

    def test_data_persistence_across_requests(self, client: TestClient):
        """Тест сохранения данных между запросами."""

        question_response = client.post(
            "/questions/", json={"text": "Тест персистентности"}
        )
        assert question_response.status_code == 201
        question_id = question_response.json()["id"]

        answer_response = client.post(
            f"/questions/{question_id}/answers/",
            json={"user_id": "persistent_user", "text": "Персистентный ответ"},
        )
        assert answer_response.status_code == 201
        answer_id = answer_response.json()["id"]

        for _ in range(3):
            question_get_response = client.get(f"/questions/{question_id}")
            assert question_get_response.status_code == 200
            question_data = question_get_response.json()
            assert question_data["text"] == "Тест персистентности"
            assert len(question_data["answers"]) == 1

            answer_get_response = client.get(f"/answers/{answer_id}")
            assert answer_get_response.status_code == 200
            answer_data = answer_get_response.json()
            assert answer_data["text"] == "Персистентный ответ"
            assert answer_data["user_id"] == "persistent_user"
            assert answer_data["question_id"] == question_id


class TestAPIPerformance:
    """Тесты производительности API."""

    @pytest.mark.parametrize("batch_size", [10, 50])
    def test_bulk_operations_performance(self, client: TestClient, batch_size):
        """Тест производительности при массовых операциях."""

        question_ids = []
        for i in range(batch_size):
            response = client.post(
                "/questions/", json={"text": f"Вопрос для теста производительности {i}"}
            )
            assert response.status_code == 201
            question_ids.append(response.json()["id"])

        for question_id in question_ids:
            for j in range(3):
                answer_data = {
                    "user_id": f"user{j}",
                    "text": f"Ответ {j} на вопрос {question_id}",
                }
                response = client.post(
                    f"/questions/{question_id}/answers/", json=answer_data
                )
                assert response.status_code == 201

        all_questions_response = client.get("/questions/")
        assert all_questions_response.status_code == 200
        all_questions = all_questions_response.json()
        assert len(all_questions) == batch_size

        for question_id in question_ids:
            question_response = client.get(f"/questions/{question_id}")
            assert question_response.status_code == 200
            question_data = question_response.json()
            assert len(question_data["answers"]) == 3
