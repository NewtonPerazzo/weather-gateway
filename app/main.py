from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.health_router import health_router
from app.routers.weather_router import weather_router
from app.routers.authentication_router import authentication_router
from app.routers.users_router import users_router
from config.settings import get_settings


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "https://weather-frontend-efh0.onrender.com",
    ],
    allow_origin_regex=r"https://.*\.onrender\.com",
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

gateway_router = APIRouter(prefix="/gateway")
gateway_router.include_router(authentication_router)
gateway_router.include_router(weather_router)
gateway_router.include_router(health_router)
gateway_router.include_router(users_router)

app.include_router(gateway_router)
