from fastapi import FastAPI
from .core.database import engine, Base
from .api import questions_router, answers_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Questions & Answers API",
    description="API-сервис для вопросов и ответов",
    version="0.1.0",
)

app.include_router(questions_router)
app.include_router(answers_router)


@app.get("/")
async def root():
    """Корневой эндпоинт."""
    return {"message": "Questions & Answers API"}


@app.get("/health")
async def health_check():
    """Проверка состояния сервиса."""
    return {"status": "healthy"}
