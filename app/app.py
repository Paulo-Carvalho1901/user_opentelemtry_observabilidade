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

from opentelemetry import trace, _logs
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

# ---------------------------------------------------------------
# 2. Define recurso da aplicação (service.name etc)
# ---------------------------------------------------------------
"""
Define metadados da aplicação para os dados de observabilidade, como:
service.name: nome do serviço
service.namespace: agrupamento lógico
service.instance.id: identificador da instância (ex: hostname)
"""
resource = Resource.create({
    "service.name": os.getenv("OTEL_SERVICE_NAME", "app"),
    "service.namespace": "observability_demo",
    "service.instance.id": os.getenv("HOSTNAME", "local"),
})

# ---------------------------------------------------------------
# 3. Configuração de TRACES
# ---------------------------------------------------------------
trace_provider = TracerProvider(resource=resource)
trace_exporter = OTLPSpanExporter(
    endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "host.docker.internal:4317"),
    insecure=os.getenv("OTEL_EXPORTER_OTLP_INSECURE", "true").lower() == "true"
)
trace_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
trace.set_tracer_provider(trace_provider)

"""
TracerProvider: gerencia os spans (eventos de rastreamento)
OTLPSpanExporter: exporta os dados via protocolo OTLP
BatchSpanProcessor: envia os dados em lote
"""

# ---------------------------------------------------------------
# 4. Configuração de LOGS (envio OTLP → Loki)
# ---------------------------------------------------------------
log_exporter = OTLPLogExporter(
    endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "host.docker.internal:4317"),
    insecure=os.getenv("OTEL_EXPORTER_OTLP_INSECURE", "true").lower() == "true"
)

logger_provider = LoggerProvider(resource=resource)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
_logs.set_logger_provider(logger_provider)

"""
Exporta logs via OTLP (por exemplo, para Loki)
Usa LoggerProvider para gerenciar os logs
BatchLogRecordProcessor envia logs em lote
"""

# Handler para redirecionar logs padrão Python → OpenTelemetry
otel_handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)

# ---------------------------------------------------------------
# 5. Configuração de logging local + integração OTEL
# ---------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - trace_id=%(otelTraceID)s span_id=%(otelSpanID)s - %(message)s"
)
root_logger = logging.getLogger()
root_logger.addHandler(otel_handler)

"""
Define o formato dos logs locais e adiciona o handler do OpenTelemetry para que os logs sejam enviados
também para o sistema de observabilidade.
"""

logger = logging.getLogger("app")
tracer = trace.get_tracer("app")

# ---------------------------------------------------------------
# 6. Imports locais e instrumentações
# ---------------------------------------------------------------
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

from .database import init_db, engine
from .routes import pessoa_routes

"""
init_db: inicializa o banco de dados
engine: conexão com o banco
pessoa_routes: rotas da API relacionadas a "pessoa"
"""

# ---------------------------------------------------------------
# 7. Ciclo de vida da aplicação
# ---------------------------------------------------------------
async def lifespan(_app: FastAPI):
    logger.info("Iniciando app e criando tabelas.")
    init_db()
    yield
    logger.info("App encerrado.")

"""
Define ações para o início e fim da aplicação:
Inicializa o banco ao iniciar
Loga quando a aplicação é encerrada
"""

# ---------------------------------------------------------------
# 8. Inicializa FastAPI + Telemetria
# ---------------------------------------------------------------
app = FastAPI(title="App Observability", lifespan=lifespan)

# Instrumentações automáticas
LoggingInstrumentor().instrument(set_logging_format=True)
FastAPIInstrumentor.instrument_app(app)
SQLAlchemyInstrumentor().instrument(engine=engine)

"""
Cria a instância do FastAPI e aplica instrumentações automáticas:
Logging
FastAPI
SQLAlchemy (ORM)
"""

# ---------------------------------------------------------------
# 9. Rotas
# Adiciona as rotas definidas no módulo pessoa_routes.
# ---------------------------------------------------------------
app.include_router(pessoa_routes.router)

# ---------------------------------------------------------------
# 10. Rota de teste para verificação de traces e logs
# ---------------------------------------------------------------
@app.get("/test-trace")
def test_trace():
    with tracer.start_as_current_span("manual-test-span"):
        logger.info("Teste de log e trace OTEL executado.")
        return {"status": "trace ok"}

# ---------------------------------------------------------------
# 11. Execução direta (modo desenvolvimento)
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
