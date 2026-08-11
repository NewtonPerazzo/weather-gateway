from fastapi import APIRouter, FastAPI

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

gateway_router = APIRouter(prefix="/gateway")
gateway_router.include_router(authentication_router)
gateway_router.include_router(weather_router)
gateway_router.include_router(health_router)
gateway_router.include_router(users_router)

app.include_router(gateway_router)
