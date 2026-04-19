import random
from fastapi import FastAPI

# Создаём экземпляр FastAPI-приложения
app = FastAPI()


# Корневой маршрут для проверки работоспособности
@app.get("/")
def read_root():
    return {"message": "Mock Spotify Recommender is running!"}


# Маршрут для получения рекомендаций по названию трека
@app.get("/api/recommend/{track_title}")
def get_fake_recommendations(track_title: str):
    fake_recommendations = []

    for i in range(5):  # генерируем 5 рекомендаций
        fake_recommendations.append({
            "track_name": f"Fake Song {i + 1} for '{track_title}'",
            "artist": f"Artist {random.randint(1, 100)}",
            "album": f"Album {random.randint(1, 20)}"
        })

    return {
        "requested_track": track_title,
        "recommendations": fake_recommendations
    }
