from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.health import router as health_router
from app.api.routes.profile import router as profile_router
from app.api.routes.recommendations import router as recommendations_router
from app.api.routes.weather import router as weather_router

api_router = APIRouter(prefix="/api")
api_router.include_router(auth_router)
api_router.include_router(profile_router)
api_router.include_router(health_router)
api_router.include_router(weather_router)
api_router.include_router(recommendations_router)
