from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import Question
from ..schemas import QuestionCreate, QuestionUpdate


class QuestionService:
    """Сервис для работы с вопросами."""

    @staticmethod
    def get_all_questions(db: Session) -> List[Question]:
        """Получить все вопросы."""
        return db.query(Question).all()

    @staticmethod
    def get_question_by_id(db: Session, question_id: int) -> Question:
        """Получить вопрос по ID."""
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Вопрос не найден"
            )
        return question

    @staticmethod
    def create_question(db: Session, question_data: QuestionCreate) -> Question:
        """Создать новый вопрос."""
        if not question_data.text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Текст вопроса не может быть пустым",
            )

        question = Question(text=question_data.text.strip())
        db.add(question)
        db.commit()
        db.refresh(question)
        return question

    @staticmethod
    def update_question(
        db: Session, question_id: int, question_data: QuestionUpdate
    ) -> Question:
        """Обновить вопрос."""
        question = QuestionService.get_question_by_id(db, question_id)

        if question_data.text is not None:
            if not question_data.text.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Текст вопроса не может быть пустым",
                )
            question.text = question_data.text.strip()

        db.commit()
        db.refresh(question)
        return question

    @staticmethod
    def delete_question(db: Session, question_id: int) -> None:
        """Удалить вопрос (каскадно удаляются все ответы)."""
        question = QuestionService.get_question_by_id(db, question_id)
        db.delete(question)
        db.commit()
