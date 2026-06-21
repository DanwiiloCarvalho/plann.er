from fastapi import APIRouter
from app.adapters.inbound.api.routes.trips import router as trips_router

router = APIRouter()

router.include_router(router=trips_router, prefix='/trips')
