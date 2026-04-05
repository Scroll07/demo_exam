from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from src.database import init_db, close_db

from src.api.base import base_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    yield
    
    await close_db()


static = StaticFiles(directory="static")

app = FastAPI(lifespan=lifespan)

app.mount("/static", static, name="static")

app.include_router(base_router, prefix="", tags=["BASE"])










