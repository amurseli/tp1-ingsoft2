import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.models
from app.database import Base, engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables ready")
    yield
    await engine.dispose()


app = FastAPI(title="eCommerce Products Service API", version="2.0.0", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}