from datetime import datetime
from typing import TYPE_CHECKING
from pydantic import BaseModel, Field, field_validator

if TYPE_CHECKING:
    from .answer import AnswerResponse


class QuestionBase(BaseModel):
    """Базовая схема вопроса."""

    text: str = Field(..., description="Текст вопроса")

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Текст вопроса не может быть пустым")
        return v.strip()


class QuestionCreate(QuestionBase):
    """Схема для создания вопроса."""

    pass


class QuestionResponse(QuestionBase):
    """Схема ответа с вопросом."""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionWithAnswers(QuestionResponse):
    """Схема вопроса с ответами."""

    answers: list["AnswerResponse"] = []

    class Config:
        from_attributes = True
