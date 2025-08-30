from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..services import AnswerService
from ..schemas import AnswerCreate, AnswerResponse

router = APIRouter(tags=["Ответы"])


@router.post(
    "/questions/{question_id}/answers/",
    response_model=AnswerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить ответ к вопросу",
    description="Создает новый ответ для указанного вопроса. Нельзя создать ответ к несуществующему вопросу. Один пользователь может оставлять несколько ответов на один вопрос.",
)
async def create_answer(
    question_id: int, answer_data: AnswerCreate, db: Session = Depends(get_db)
):
    """Добавить ответ к вопросу."""
    answer = AnswerService.create_answer(db, question_id, answer_data)
    return answer


@router.get(
    "/answers/{answer_id}",
    response_model=AnswerResponse,
    summary="Получить ответ по ID",
    description="Возвращает конкретный ответ по его идентификатору. Если ответ не найден, возвращает ошибку 404.",
)
async def get_answer(answer_id: int, db: Session = Depends(get_db)):
    """Получить конкретный ответ."""
    answer = AnswerService.get_answer_by_id(db, answer_id)
    return answer


@router.delete(
    "/answers/{answer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить ответ",
    description="Удаляет конкретный ответ по его идентификатору. Если ответ не найден, возвращает ошибку 404.",
)
async def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    """Удалить ответ."""
    AnswerService.delete_answer(db, answer_id)
    return None
