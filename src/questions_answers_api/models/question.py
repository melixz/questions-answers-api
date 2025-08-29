from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from ..core.database import Base


class Question(Base):
    """Модель вопроса."""

    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    answers = relationship(
        "Answer", back_populates="question", cascade="all, delete-orphan"
    )
