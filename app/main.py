from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.router import router

app = FastAPI()
app.include_router(router=router, prefix=str(settings.API_PREFIX))
