import pytest
from datetime import datetime
from pydantic import ValidationError
from src.questions_answers_api.schemas import (
    QuestionCreate,
    QuestionResponse,
    QuestionWithAnswers,
    AnswerCreate,
    AnswerResponse,
)


class TestQuestionSchemas:
    """Тесты схем для вопросов."""

    def test_question_create_valid(self):
        """Тест валидной схемы создания вопроса."""
        data = {"text": "Что такое Python?"}
        schema = QuestionCreate(**data)

        assert schema.text == "Что такое Python?"

    @pytest.mark.parametrize(
        "invalid_text",
        [
            "",
            "   ",
            "\t\n",
            None,
        ],
    )
    def test_question_create_invalid_text(self, invalid_text):
        """Тест невалидного текста в схеме создания вопроса."""
        data = {"text": invalid_text}

        with pytest.raises(ValidationError):
            QuestionCreate(**data)

    def test_question_create_text_stripping(self):
        """Тест автоматической обрезки пробелов в тексте вопроса."""
        data = {"text": "  Вопрос с пробелами  "}
        schema = QuestionCreate(**data)

        assert schema.text == "Вопрос с пробелами"

    def test_question_response_schema(self):
        """Тест схемы ответа для вопроса."""
        data = {
            "id": 1,
            "text": "Тестовый вопрос",
            "created_at": datetime.now(),
        }
        schema = QuestionResponse(**data)

        assert schema.id == 1
        assert schema.text == "Тестовый вопрос"
        assert isinstance(schema.created_at, datetime)

    def test_question_with_answers_schema(self):
        """Тест схемы вопроса с ответами."""
        answer_data = {
            "id": 1,
            "question_id": 1,
            "user_id": "user123",
            "text": "Тестовый ответ",
            "created_at": datetime.now(),
        }

        data = {
            "id": 1,
            "text": "Тестовый вопрос",
            "created_at": datetime.now(),
            "answers": [answer_data],
        }

        schema = QuestionWithAnswers(**data)

        assert schema.id == 1
        assert schema.text == "Тестовый вопрос"
        assert len(schema.answers) == 1
        assert schema.answers[0].id == 1
        assert schema.answers[0].text == "Тестовый ответ"


class TestAnswerSchemas:
    """Тесты схем для ответов."""

    def test_answer_create_valid(self):
        """Тест валидной схемы создания ответа."""
        data = {
            "user_id": "user123",
            "text": "Это отличный ответ!",
        }
        schema = AnswerCreate(**data)

        assert schema.user_id == "user123"
        assert schema.text == "Это отличный ответ!"

    @pytest.mark.parametrize(
        "invalid_field,invalid_value",
        [
            ("user_id", ""),
            ("user_id", "   "),
            ("user_id", None),
            ("text", ""),
            ("text", "   "),
            ("text", None),
        ],
    )
    def test_answer_create_invalid_fields(self, invalid_field, invalid_value):
        """Тест невалидных полей в схеме создания ответа."""
        valid_data = {
            "user_id": "user123",
            "text": "Валидный текст",
        }
        valid_data[invalid_field] = invalid_value

        with pytest.raises(ValidationError):
            AnswerCreate(**valid_data)

    def test_answer_create_long_text(self):
        """Тест создания ответа с длинным текстом."""
        long_text = "А" * 1000
        data = {
            "user_id": "user123",
            "text": long_text,
        }
        schema = AnswerCreate(**data)

        assert schema.text == long_text
        assert len(schema.text) == 1000

    def test_answer_response_schema(self):
        """Тест схемы ответа для ответа."""
        data = {
            "id": 1,
            "question_id": 1,
            "user_id": "user123",
            "text": "Тестовый ответ",
            "created_at": datetime.now(),
        }
        schema = AnswerResponse(**data)

        assert schema.id == 1
        assert schema.question_id == 1
        assert schema.user_id == "user123"
        assert schema.text == "Тестовый ответ"
        assert isinstance(schema.created_at, datetime)

    @pytest.mark.parametrize(
        "user_id",
        [
            "simple_user",
            "user_with_numbers123",
            "user-with-dashes",
            "user.with.dots",
            "user_with_underscores",
            "UPPERCASE_USER",
            "MixedCase_User",
        ],
    )
    def test_answer_create_various_user_ids(self, user_id):
        """Тест создания ответов с различными форматами user_id."""
        data = {
            "user_id": user_id,
            "text": "Тестовый ответ",
        }
        schema = AnswerCreate(**data)

        assert schema.user_id == user_id


class TestSchemaValidation:
    """Тесты валидации схем."""

    def test_missing_required_fields(self):
        """Тест отсутствующих обязательных полей."""

        with pytest.raises(ValidationError) as exc_info:
            QuestionCreate()
        assert "text" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            AnswerCreate(text="Текст без пользователя")
        assert "user_id" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            AnswerCreate(user_id="user123")
        assert "text" in str(exc_info.value)

    def test_extra_fields_ignored(self):
        """Тест игнорирования дополнительных полей."""

        data = {
            "text": "Вопрос",
            "extra_field": "должно игнорироваться",
            "another_extra": 123,
        }
        schema = QuestionCreate(**data)
        assert schema.text == "Вопрос"
        assert not hasattr(schema, "extra_field")
        assert not hasattr(schema, "another_extra")

    def test_type_coercion(self):
        """Тест автоматического преобразования типов."""

        data = {
            "user_id": 123,
            "text": "Тестовый ответ",
        }
        schema = AnswerCreate(**data)
        assert schema.user_id == "123"

    @pytest.mark.parametrize(
        "schema_class,valid_data",
        [
            (QuestionCreate, {"text": "Тест"}),
            (AnswerCreate, {"user_id": "user", "text": "Ответ"}),
        ],
    )
    def test_schema_serialization(self, schema_class, valid_data):
        """Тест сериализации схем в JSON."""
        schema = schema_class(**valid_data)

        json_data = schema.model_dump()
        assert isinstance(json_data, dict)

        new_schema = schema_class(**json_data)
        assert new_schema == schema

    def test_datetime_handling(self):
        """Тест обработки datetime полей."""
        now = datetime.now()

        question_data = {
            "id": 1,
            "text": "Вопрос с датой",
            "created_at": now,
        }
        question_schema = QuestionResponse(**question_data)
        assert question_schema.created_at == now

        answer_data = {
            "id": 1,
            "question_id": 1,
            "user_id": "user123",
            "text": "Ответ с датой",
            "created_at": now,
        }
        answer_schema = AnswerResponse(**answer_data)
        assert answer_schema.created_at == now
