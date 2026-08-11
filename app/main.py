from fastapi import FastAPI

from app.routers.health_router import health_router
from config.settings import get_settings


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)

app.include_router(health_router)
