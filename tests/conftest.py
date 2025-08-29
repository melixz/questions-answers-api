import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from src.questions_answers_api.core.database import Base, get_db
from src.questions_answers_api.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Переопределение зависимости базы данных для тестов."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    """Фикстура клиента для тестов."""
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_question_data():
    """Фикстура с данными для создания вопроса."""
    return {"text": "Что такое Python?"}


@pytest.fixture
def sample_answer_data():
    """Фикстура с данными для создания ответа."""
    return {"user_id": "user123", "text": "Python - это язык программирования"}


@pytest.fixture
def created_question(client, sample_question_data):
    """Фикстура для создания вопроса в БД."""
    response = client.post("/questions/", json=sample_question_data)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def created_answer(client, created_question, sample_answer_data):
    """Фикстура для создания ответа в БД."""
    question_id = created_question["id"]
    response = client.post(
        f"/questions/{question_id}/answers/", json=sample_answer_data
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def multiple_questions(client):
    """Фикстура для создания нескольких вопросов."""
    questions = []
    for i in range(3):
        response = client.post("/questions/", json={"text": f"Вопрос {i + 1}"})
        assert response.status_code == 201
        questions.append(response.json())
    return questions


@pytest.fixture
def question_with_answers(client, created_question):
    """Фикстура для создания вопроса с несколькими ответами."""
    question_id = created_question["id"]
    answers = []

    for i in range(2):
        answer_data = {"user_id": f"user{i + 1}", "text": f"Ответ {i + 1}"}
        response = client.post(f"/questions/{question_id}/answers/", json=answer_data)
        assert response.status_code == 201
        answers.append(response.json())

    return {"question": created_question, "answers": answers}
