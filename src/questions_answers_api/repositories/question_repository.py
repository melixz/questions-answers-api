from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import Question


class QuestionRepository:
    """Репозиторий для работы с вопросами в базе данных."""

    def __init__(self, db: Session):
        """Инициализация репозитория."""
        self.db = db

    def get_all(self) -> List[Question]:
        """Получить все вопросы."""
        return self.db.query(Question).all()

    def get_by_id(self, question_id: int) -> Optional[Question]:
        """Получить вопрос по ID."""
        return self.db.query(Question).filter(Question.id == question_id).first()

    def create(self, text: str) -> Question:
        """Создать новый вопрос."""
        question = Question(text=text)
        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)
        return question

    def update(self, question: Question, text: str) -> Question:
        """Обновить вопрос."""
        question.text = text
        self.db.commit()
        self.db.refresh(question)
        return question

    def delete(self, question: Question) -> None:
        """Удалить вопрос."""
        self.db.delete(question)
        self.db.commit()

    def exists(self, question_id: int) -> bool:
        """Проверить существование вопроса."""
        return (
            self.db.query(Question).filter(Question.id == question_id).first()
            is not None
        )
