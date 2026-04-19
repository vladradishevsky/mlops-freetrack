from fastapi import FastAPI, HTTPException, Query
from recommender import load_model, recommend_songs
from schemas import RecommendationResponse
from typing import List


# Инициализация приложения с метаданными для документации
app = FastAPI(
    title="Spotify Recommender API",
    description="Получи рекомендации похожих песен по названию трека на основе косинусного сходства.",
    version="1.0.0",
    contact={
        "name": "Your Name",  # Используйте общее имя или организации, предоставляющей сервис
        "email": "your_email@example.com"  # Общий email
    }
)

# Загрузка модели при старте сервера (выполняется один раз)
model = load_model()


@app.get("/", tags=["Health Check"])
def read_root():
    return {"message": "🎶 Music Recommender is running!"}


# Основной маршрут для получения рекомендаций
@app.get(
    "/api/recommend/",
    response_model=RecommendationResponse,
    summary="Получить рекомендации по песне",
    description="Возвращает список песен, похожих на указанную, используя косинусное сходство по признакам.",
    tags=["Recommendations"]
)
def get_recommendations(
    track_title: str = Query(..., description="Название песни для поиска"),
    N: int = Query(5, alias="n", ge=1, le=20, description="Количество рекомендаций (от 1 до 20)")
):
    recommendations = recommend_songs(model, track_title, N)

    if not recommendations:
        raise HTTPException(
            status_code=404,
            detail=f"Трек '{track_title}' не найден в базе данных."
        )

    return {"requested_track": track_title, "recommendations": recommendations}
