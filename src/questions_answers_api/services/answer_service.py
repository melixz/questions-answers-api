from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import Answer
from ..schemas import AnswerCreate
from ..repositories.answer_repository import AnswerRepository
from ..repositories.question_repository import QuestionRepository


class AnswerService:
    """Сервис для работы с ответами."""

    @staticmethod
    def get_answer_by_id(db: Session, answer_id: int) -> Answer:
        """Получить ответ по ID."""
        repo = AnswerRepository(db)
        answer = repo.get_by_id(answer_id)
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
        question_repo = QuestionRepository(db)
        if not question_repo.exists(question_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Вопрос не найден"
            )

        answer_repo = AnswerRepository(db)
        return answer_repo.create(question_id, answer_data.user_id, answer_data.text)

    @staticmethod
    def delete_answer(db: Session, answer_id: int) -> None:
        """Удалить ответ."""
        repo = AnswerRepository(db)
        answer = repo.get_by_id(answer_id)
        if not answer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Ответ не найден"
            )
        repo.delete(answer)
