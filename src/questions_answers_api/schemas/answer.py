from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class AnswerBase(BaseModel):
    """Базовая схема ответа."""

    user_id: str = Field(..., description="Идентификатор пользователя")
    text: str = Field(..., description="Текст ответа")

    @field_validator("user_id", mode="before")
    @classmethod
    def validate_user_id(cls, v) -> str:
        # Convert to string if not already
        v_str = str(v) if v is not None else ""
        if not v_str or not v_str.strip():
            raise ValueError("Идентификатор пользователя не может быть пустым")
        return v_str.strip()

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Текст ответа не может быть пустым")
        return v.strip()


class AnswerCreate(AnswerBase):
    """Схема для создания ответа."""

    pass


class AnswerResponse(AnswerBase):
    """Схема ответа с ответом."""

    id: int
    question_id: int
    created_at: datetime

    class Config:
        from_attributes = True
