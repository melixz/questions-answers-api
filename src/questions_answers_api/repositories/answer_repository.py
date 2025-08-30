from typing import Optional
from sqlalchemy.orm import Session
from ..models import Answer


class AnswerRepository:
    """Репозиторий для работы с ответами в базе данных."""

    def __init__(self, db: Session):
        """Инициализация репозитория."""
        self.db = db

    def get_by_id(self, answer_id: int) -> Optional[Answer]:
        """Получить ответ по ID."""
        return self.db.query(Answer).filter(Answer.id == answer_id).first()

    def get_by_question_id(self, question_id: int) -> list[Answer]:
        """Получить все ответы для вопроса."""
        return self.db.query(Answer).filter(Answer.question_id == question_id).all()

    def create(self, question_id: int, user_id: str, text: str) -> Answer:
        """Создать новый ответ."""
        answer = Answer(question_id=question_id, user_id=user_id, text=text)
        self.db.add(answer)
        self.db.commit()
        self.db.refresh(answer)
        return answer

    def delete(self, answer: Answer) -> None:
        """Удалить ответ."""
        self.db.delete(answer)
        self.db.commit()

    def exists(self, answer_id: int) -> bool:
        """Проверить существование ответа."""
        return self.db.query(Answer).filter(Answer.id == answer_id).first() is not None
