from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..services import QuestionService
from ..schemas import (
    QuestionCreate,
    QuestionResponse,
    QuestionWithAnswers,
)

router = APIRouter(prefix="/questions", tags=["Вопросы"])


@router.get(
    "/",
    response_model=list[QuestionResponse],
    summary="Получить все вопросы",
    description="Возвращает список всех вопросов в системе. Если вопросов нет, возвращает пустой список.",
)
async def get_all_questions(db: Session = Depends(get_db)):
    """Получить список всех вопросов."""
    questions = QuestionService.get_all_questions(db)
    return questions


@router.post(
    "/",
    response_model=QuestionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый вопрос",
    description="Создает новый вопрос в системе. Текст вопроса не может быть пустым или состоять только из пробелов.",
)
async def create_question(question_data: QuestionCreate, db: Session = Depends(get_db)):
    """Создать новый вопрос."""
    question = QuestionService.create_question(db, question_data)
    return question


@router.get(
    "/{question_id}",
    response_model=QuestionWithAnswers,
    summary="Получить вопрос с ответами",
    description="Возвращает конкретный вопрос со всеми ответами на него. Если вопрос не найден, возвращает ошибку 404.",
)
async def get_question_with_answers(question_id: int, db: Session = Depends(get_db)):
    """Получить вопрос и все ответы на него."""
    question = QuestionService.get_question_by_id(db, question_id)
    return question


@router.delete(
    "/{question_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить вопрос",
    description="Удаляет вопрос и все связанные с ним ответы (каскадное удаление). Если вопрос не найден, возвращает ошибку 404.",
)
async def delete_question(question_id: int, db: Session = Depends(get_db)):
    """Удалить вопрос (вместе с ответами)."""
    QuestionService.delete_question(db, question_id)
    return None
