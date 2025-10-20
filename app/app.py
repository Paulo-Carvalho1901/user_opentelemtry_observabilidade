import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from opentelemetry.trace import get_tracer

from database import init_db, drop_db
from .routes import pessoa_routes


logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


tracer = get_tracer('app')


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('iniciando app...')
    init_db()
    yield
    logger.info('Encerrando app...')
    drop_db()

app = FastAPI(title='App Observability', lifespan=lifespan)

app.include_router(pessoa_routes.router)
