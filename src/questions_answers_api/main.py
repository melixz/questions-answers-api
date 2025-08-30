from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .api import questions_router, answers_router

app = FastAPI(
    title="Questions & Answers API",
    description="API-сервис для вопросов и ответов",
    version="0.1.0",
)

app.include_router(questions_router)
app.include_router(answers_router)


@app.get("/", include_in_schema=False)
async def root():
    """Редирект на документацию API."""
    return RedirectResponse(url="/docs")


@app.get(
    "/health",
    summary="Проверка здоровья сервиса",
    description="Эндпоинт для проверки работоспособности API сервиса",
    tags=["System"],
)
async def health_check():
    """Проверка состояния сервиса."""
    return {"status": "healthy", "message": "API работает нормально"}
