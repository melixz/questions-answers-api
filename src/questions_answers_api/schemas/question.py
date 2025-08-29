from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class QuestionBase(BaseModel):
    """Базовая схема вопроса."""

    text: str = Field(..., min_length=1, description="Текст вопроса")


class QuestionCreate(QuestionBase):
    """Схема для создания вопроса."""

    pass


class QuestionUpdate(BaseModel):
    """Схема для обновления вопроса."""

    text: Optional[str] = Field(None, min_length=1, description="Новый текст вопроса")


class QuestionResponse(QuestionBase):
    """Схема ответа с вопросом."""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionWithAnswers(QuestionResponse):
    """Схема вопроса с ответами."""

    from .answer import AnswerResponse

    answers: List[AnswerResponse] = []

    class Config:
        from_attributes = True
