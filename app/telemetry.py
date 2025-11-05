import os
import logging
from dotenv import load_dotenv

from opentelemetry import trace, _logs, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.metrics import Observation
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

from .database import SessionLocal
from .models import Pessoa

# ---------------------------------------------------------------
# 1. Carrega variaveis de ambiente
# ---------------------------------------------------------------
load_dotenv(dotenv_path="./.env")

# ---------------------------------------------------------------
# 2. Define recurso da aplicae7e3o
# ---------------------------------------------------------------
resource = Resource.create({
    "service.name": os.getenv("OTEL_SERVICE_NAME", "app"),
    "service.namespace": "observability_demo",
    "service.instance.id": os.getenv("HOSTNAME", "local"),
})

# ---------------------------------------------------------------
# 3. Configurae7e3o de TRACES
# ---------------------------------------------------------------
trace_provider = TracerProvider(resource=resource)
trace_exporter = OTLPSpanExporter(
    endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "host.docker.internal:4317"),
    insecure=os.getenv("OTEL_EXPORTER_OTLP_INSECURE", "true").lower() == "true"
)
trace_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
trace.set_tracer_provider(trace_provider)
tracer = trace.get_tracer("app")

# ---------------------------------------------------------------
# 4. Configurae7e3o de LOGS
# ---------------------------------------------------------------
log_exporter = OTLPLogExporter(
    endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "host.docker.internal:4317"),
    insecure=os.getenv("OTEL_EXPORTER_OTLP_INSECURE", "true").lower() == "true"
)
logger_provider = LoggerProvider(resource=resource)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
_logs.set_logger_provider(logger_provider)

otel_handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - trace_id=%(otelTraceID)s span_id=%(otelSpanID)s - %(message)s"
)
logger = logging.getLogger("app")
logger.addHandler(otel_handler)

# ---------------------------------------------------------------
# 5. Configurae7e3o de Me9tricas
# ---------------------------------------------------------------
metric_exporter = OTLPMetricExporter(
    endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "host.docker.internal:4317"),
    insecure=os.getenv("OTEL_EXPORTER_OTLP_INSECURE", "true").lower() == "true"
)
metric_reader = PeriodicExportingMetricReader(metric_exporter)
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter("app")

users_created_counter = meter.create_counter(
    name="users_created",
    description="Nfamero de usue1rios criados",
    unit="1"
)

def usuarios_ativos_callback(options):
    db = SessionLocal()
    try:
        count = db.query(Pessoa).filter(Pessoa.activo == True).count()
    finally:
        db.close()
    return [Observation(count, {})]

usuarios_ativos_gauge = meter.create_observable_gauge(
    name="usuarios_ativos",
    description="Nfamero atual de usue1rios ativos no sistema",
    unit="1",
    callbacks=[usuarios_ativos_callback]
)

# ---------------------------------------------------------------
# 6. Setup para ser chamado no app.py
# ---------------------------------------------------------------
def setup_telemetry():
    pass  # Mantido para compatibilidade e inicializae7e3o expledcita
