"""
app/app.py
Arquivo principal da aplicação FastAPI.

Funções:
- Carrega .env
- Inicializa FastAPI com lifespan (cria/destroi tabelas)
- Aplica instrumentação OpenTelemetry (logging, FastAPI, SQLAlchemy)
- Inclui rotas do módulo pessoa_routes
"""

import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv

# ===============================================================
# 1️⃣ Carrega variáveis de ambiente (.env)
# ===============================================================
# Deve ser executado ANTES de inicializar o OpenTelemetry
load_dotenv(dotenv_path="./.env")

# ===============================================================
# 2️⃣ Configura o TracerProvider explicitamente
# ===============================================================
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Define o service.name (do .env) ou usa 'app' como padrão
resource = Resource.create({
    "service.name": os.getenv("OTEL_SERVICE_NAME", "app"),
    "service.namespace": "observability_demo",
    "service.instance.id": os.getenv("HOSTNAME", "local"),
})

# Configura o provider e exportador OTLP
trace_provider = TracerProvider(resource=resource)
trace_exporter = OTLPSpanExporter(
    endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "grpc://host.docker.internal:4317"),
    insecure=os.getenv("OTEL_EXPORTER_OTLP_INSECURE", "true").lower() == "true"
)
trace_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
trace.set_tracer_provider(trace_provider)

# ===============================================================
# 3️⃣ Importa instrumentações do OpenTelemetry
# ===============================================================
from opentelemetry.trace import get_tracer
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# ===============================================================
# 4️⃣ Imports locais (somente após dotenv)
# ===============================================================
from .database import init_db, drop_db, engine
from .routes import pessoa_routes  # certifique-se que o arquivo é pessoa_routes.py

# ===============================================================
# 5️⃣ Configuração de logs padrão
# ===============================================================
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s"))
    logger.addHandler(handler)

# ===============================================================
# 6️⃣ Cria tracer manual (para spans customizados)
# ===============================================================
tracer = get_tracer("app")

# ===============================================================
# 7️⃣ Lifespan da aplicação
# ===============================================================
@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("🚀 Iniciando app... criando tabelas.")
    init_db()
    yield
    logger.info("🧹 Encerrando app... limpando recursos (opcional).")
    drop_db()  # pode comentar se não quiser limpar o banco no shutdown

# ===============================================================
# 8️⃣ Inicializa a aplicação FastAPI
# ===============================================================
app = FastAPI(title="App Observability", lifespan=lifespan)

# ===============================================================
# 9️⃣ Instrumentação OpenTelemetry
# ===============================================================
LoggingInstrumentor().instrument(set_logging_format=True)
FastAPIInstrumentor.instrument_app(app)
SQLAlchemyInstrumentor().instrument(engine=engine)

# ===============================================================
# 🔟 Registra rotas
# ===============================================================
app.include_router(pessoa_routes.router)

# ===============================================================
# 1️⃣1️⃣ Rota de teste para forçar logs + spans
# ===============================================================
@app.get("/test-trace")
def test_trace():
    """
    Gera um log e um span manual para verificar se o Grafana está recebendo traces.
    """
    with tracer.start_as_current_span("manual-test-span"):
        logger.info("📡 Teste de log OTEL - manual-test-span")
        return {"status": "trace ok"}

# Star da aplicação python -m app.app
# ===============================================================
# 1️⃣2️⃣ Execução direta (opcional) 
# ===============================================================
if __name__ == "__main__":
    import uvicorn

    # --- Reaplica instrumentação caso rode direto ---
    # (Garantindo que logs, FastAPI e SQLAlchemy ainda geram spans)
    LoggingInstrumentor().instrument(set_logging_format=True)
    FastAPIInstrumentor.instrument_app(app)
    SQLAlchemyInstrumentor().instrument(engine=engine)

    uvicorn.run(
        "app.app:app",  # caminho do módulo e nome do objeto FastAPI
        host="0.0.0.0",
        port=8000,
        reload=True,   # hot reload em desenvolvimento
        log_level="info"
    )
