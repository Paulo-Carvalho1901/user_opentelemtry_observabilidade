"""
app/app.py
Aplicação FastAPI com observabilidade via OpenTelemetry.
"""

import os
import logging
from fastapi import FastAPI
from dotenv import load_dotenv

# ---------------------------------------------------------------
# 1. Configura ambiente e recursos
# ---------------------------------------------------------------
load_dotenv(dotenv_path="./.env")

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

resource = Resource.create({
    "service.name": os.getenv("OTEL_SERVICE_NAME", "app"),
    "service.namespace": "observability_demo",
    "service.instance.id": os.getenv("HOSTNAME", "local"),
})

trace_provider = TracerProvider(resource=resource)
trace_exporter = OTLPSpanExporter(
    endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "host.docker.internal:4317"),
    insecure=os.getenv("OTEL_EXPORTER_OTLP_INSECURE", "true").lower() == "true"
)
trace_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
trace.set_tracer_provider(trace_provider)

# ---------------------------------------------------------------
# 2. Imports locais e instrumentações
# ---------------------------------------------------------------
from opentelemetry.trace import get_tracer
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

from .database import init_db, engine
from .routes import pessoa_routes


# ---------------------------------------------------------------
# 3. Configuração de logging
# ---------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s"
)
logger = logging.getLogger("app")
tracer = get_tracer("app")

# ---------------------------------------------------------------
# 4. Ciclo de vida da aplicação
# ---------------------------------------------------------------
async def lifespan(_app: FastAPI):
    logger.info("Iniciando app e criando tabelas.")
    init_db()
    yield
    logger.info("App encerrado.")

# ---------------------------------------------------------------
# 5. Inicializa FastAPI + Telemetria
# ---------------------------------------------------------------
app = FastAPI(title="App Observability", lifespan=lifespan)


# ---------------------------------------------------------------
# 6. Instrumentação OpenTelemetry
# ---------------------------------------------------------------
LoggingInstrumentor().instrument(set_logging_format=True)
FastAPIInstrumentor.instrument_app(app)
SQLAlchemyInstrumentor().instrument(engine=engine)

# ---------------------------------------------------------------
# 7. Rotas
# ---------------------------------------------------------------
app.include_router(pessoa_routes.router)

# ---------------------------------------------------------------
# 8. Rota de teste para verificação de traces
# ---------------------------------------------------------------
@app.get("/test-trace")
def test_trace():
    with tracer.start_as_current_span("manual-test-span"):
        logger.info("Teste de log e trace OTEL executado.")
        return {"status": "trace ok"}

# ---------------------------------------------------------------
# 9. Execução direta (modo desenvolvimento)
# ---------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
