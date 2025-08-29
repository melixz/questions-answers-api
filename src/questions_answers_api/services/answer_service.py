from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import Answer, Question
from ..schemas import AnswerCreate, AnswerUpdate


class AnswerService:
    """Сервис для работы с ответами."""

    @staticmethod
    def get_answer_by_id(db: Session, answer_id: int) -> Answer:
        """Получить ответ по ID."""
        answer = db.query(Answer).filter(Answer.id == answer_id).first()
        if not answer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Ответ не найден"
            )
        return answer

    @staticmethod
    def create_answer(
        db: Session, question_id: int, answer_data: AnswerCreate
    ) -> Answer:
        """Создать новый ответ к вопросу."""
        # Проверяем существование вопроса
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Вопрос не найден"
            )

        # Валидация данных
        if not answer_data.text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Текст ответа не может быть пустым",
            )

        if not answer_data.user_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Идентификатор пользователя не может быть пустым",
            )

        answer = Answer(
            question_id=question_id,
            user_id=answer_data.user_id.strip(),
            text=answer_data.text.strip(),
        )
        db.add(answer)
        db.commit()
        db.refresh(answer)
        return answer

    @staticmethod
    def update_answer(db: Session, answer_id: int, answer_data: AnswerUpdate) -> Answer:
        """Обновить ответ."""
        answer = AnswerService.get_answer_by_id(db, answer_id)

        if answer_data.text is not None:
            if not answer_data.text.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Текст ответа не может быть пустым",
                )
            answer.text = answer_data.text.strip()

        db.commit()
        db.refresh(answer)
        return answer

    @staticmethod
    def delete_answer(db: Session, answer_id: int) -> None:
        """Удалить ответ."""
        answer = AnswerService.get_answer_by_id(db, answer_id)
        db.delete(answer)
        db.commit()
