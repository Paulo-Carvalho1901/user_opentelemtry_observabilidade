import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from opentelemetry.trace import get_tracer
from dotenv import load_dotenv 
import os

from .database import init_db, drop_db
from .routes import pessoa_routes

# Carregando as variavel de ambiente
load_dotenv() # isso lê o arquivo .env automaticamente
# Agora OTEL_* já estão disponíveis em os.environ
# Exemplo: print(os.getenv("OTEL_SERVICE_NAME"))

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from .database import engine


logger = logging.getLogger('app')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


tracer = get_tracer('app')


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info('iniciando app...')
    init_db()
    yield
    logger.info('Encerrando app...')
    drop_db()

app = FastAPI(title='App Observability', lifespan=lifespan)

# --- Instrumentação ---
LoggingInstrumentor().instrument(set_logging_format=True, log_level=logging.INFO)
FastAPIInstrumentor.instrument_app(app)
SQLAlchemyInstrumentor().instrument(engine=engine)

app.include_router(pessoa_routes.router)


# Comando para iniciar
# docker compose up -d
# opentelemetry-bootstrap -a install
# opentelemetry-instrument venv\Scripts\uvicorn.exe app.app:app --reload --port 8000
