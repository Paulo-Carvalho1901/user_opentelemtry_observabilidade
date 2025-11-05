import logging
from fastapi import FastAPI
from .database import init_db, engine
from .routes import rotas_pessoas
from .telemetry import setup_telemetry

# ---------------------------------------------------------------
# 1. Inicializa a telemetria
# ---------------------------------------------------------------
setup_telemetry()

# ---------------------------------------------------------------
# 2. Ciclo de vida da aplicação
# ---------------------------------------------------------------
async def lifespan(_app: FastAPI):
    logging.getLogger("app").info("Iniciando app e criando tabelas.")
    init_db()
    yield
    logging.getLogger("app").info("App encerrado.")

# ---------------------------------------------------------------
# 3. Inicializa FastAPI + Instrumentações
# ---------------------------------------------------------------
app = FastAPI(title="App Observability", lifespan=lifespan)

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

FastAPIInstrumentor.instrument_app(app)
LoggingInstrumentor().instrument(set_logging_format=True)
SQLAlchemyInstrumentor().instrument(engine=engine)

# ---------------------------------------------------------------
# 4. Rotas
# ---------------------------------------------------------------
app.include_router(rotas_pessoas.router)

# ---------------------------------------------------------------
# 5. Rota de teste
# ---------------------------------------------------------------
from .telemetry import tracer, logger

@app.get("/test-trace")
def test_trace():
    with tracer.start_as_current_span("manual-test-span"):
        logger.info("Teste de log e trace OTEL executado.")
        return {"status": "trace ok"}

# ---------------------------------------------------------------
# 6. Execução direta
# ---------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
