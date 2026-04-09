from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from src.config import config
from src.database import init_db, close_db
from src.api.base import base_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    yield
    
    await close_db()


static = StaticFiles(directory="static")


app = FastAPI(lifespan=lifespan)

app.add_middleware(SessionMiddleware, secret_key=config.SESSION_MIDDLEWARE_KEY)

app.mount("/static", static, name="static")

app.include_router(base_router, prefix="", tags=["BASE"])










