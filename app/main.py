from fastapi import FastAPI
from app.infrastructure.config import settings
from app.adapters.inbound.api.router import router as api_router

app = FastAPI()
app.include_router(router=api_router, prefix=str(settings.API_PREFIX))
