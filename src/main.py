from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.database import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    yield
    
    await close_db()


app = FastAPI(lifespan=lifespan)











