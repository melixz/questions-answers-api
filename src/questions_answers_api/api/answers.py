from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..services import AnswerService
from ..schemas import AnswerCreate, AnswerUpdate, AnswerResponse

router = APIRouter(tags=["answers"])


@router.post(
    "/questions/{question_id}/answers/",
    response_model=AnswerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_answer(
    question_id: int, answer_data: AnswerCreate, db: Session = Depends(get_db)
):
    """Добавить ответ к вопросу."""
    answer = AnswerService.create_answer(db, question_id, answer_data)
    return answer


@router.get("/answers/{answer_id}", response_model=AnswerResponse)
async def get_answer(answer_id: int, db: Session = Depends(get_db)):
    """Получить конкретный ответ."""
    answer = AnswerService.get_answer_by_id(db, answer_id)
    return answer


@router.put("/answers/{answer_id}", response_model=AnswerResponse)
async def update_answer(
    answer_id: int, answer_data: AnswerUpdate, db: Session = Depends(get_db)
):
    """Обновить ответ."""
    answer = AnswerService.update_answer(db, answer_id, answer_data)
    return answer


@router.delete("/answers/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    """Удалить ответ."""
    AnswerService.delete_answer(db, answer_id)
    return None
