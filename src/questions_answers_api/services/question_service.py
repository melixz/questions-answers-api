from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import Question
from ..schemas import QuestionCreate
from ..repositories.question_repository import QuestionRepository


class QuestionService:
    """Сервис для работы с вопросами."""

    @staticmethod
    def get_all_questions(db: Session) -> list[Question]:
        """Получить все вопросы."""
        repo = QuestionRepository(db)
        return repo.get_all()

    @staticmethod
    def get_question_by_id(db: Session, question_id: int) -> Question:
        """Получить вопрос по ID."""
        repo = QuestionRepository(db)
        question = repo.get_by_id(question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Вопрос не найден"
            )
        return question

    @staticmethod
    def create_question(db: Session, question_data: QuestionCreate) -> Question:
        """Создать новый вопрос."""
        repo = QuestionRepository(db)
        return repo.create(question_data.text)

    @staticmethod
    def delete_question(db: Session, question_id: int) -> None:
        """Удалить вопрос (каскадно удаляются все ответы)."""
        repo = QuestionRepository(db)
        question = repo.get_by_id(question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Вопрос не найден"
            )
        repo.delete(question)
