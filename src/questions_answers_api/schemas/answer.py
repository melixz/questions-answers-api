from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AnswerBase(BaseModel):
    """Базовая схема ответа."""

    user_id: str = Field(..., description="Идентификатор пользователя")
    text: str = Field(..., min_length=1, description="Текст ответа")


class AnswerCreate(AnswerBase):
    """Схема для создания ответа."""

    pass


class AnswerUpdate(BaseModel):
    """Схема для обновления ответа."""

    text: Optional[str] = Field(None, min_length=1, description="Новый текст ответа")


class AnswerResponse(AnswerBase):
    """Схема ответа с ответом."""

    id: int
    question_id: int
    created_at: datetime

    class Config:
        from_attributes = True
