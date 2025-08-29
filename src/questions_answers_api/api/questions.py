from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..services import QuestionService
from ..schemas import (
    QuestionCreate,
    QuestionUpdate,
    QuestionResponse,
    QuestionWithAnswers,
)

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=List[QuestionResponse])
async def get_all_questions(db: Session = Depends(get_db)):
    """Получить список всех вопросов."""
    questions = QuestionService.get_all_questions(db)
    return questions


@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(question_data: QuestionCreate, db: Session = Depends(get_db)):
    """Создать новый вопрос."""
    question = QuestionService.create_question(db, question_data)
    return question


@router.get("/{question_id}", response_model=QuestionWithAnswers)
async def get_question_with_answers(question_id: int, db: Session = Depends(get_db)):
    """Получить вопрос и все ответы на него."""
    question = QuestionService.get_question_by_id(db, question_id)
    return question


@router.put("/{question_id}", response_model=QuestionResponse)
async def update_question(
    question_id: int, question_data: QuestionUpdate, db: Session = Depends(get_db)
):
    """Обновить вопрос."""
    question = QuestionService.update_question(db, question_id, question_data)
    return question


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(question_id: int, db: Session = Depends(get_db)):
    """Удалить вопрос (вместе с ответами)."""
    QuestionService.delete_question(db, question_id)
    return None
