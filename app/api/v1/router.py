from fastapi import APIRouter
from app.api.v1.endpoints import trips

router = APIRouter()

router.include_router(router=trips.router, prefix='/trips')
