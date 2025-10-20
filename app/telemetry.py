# app/telemetry.py
from prometheus_client import start_http_server
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from app.database import engine
import logging

logger = logging.getLogger("telemetry")

def setup_telemetry(app):
    """
    Configura a coleta de métricas Prometheus e instrumentação de FastAPI/SQLAlchemy.
    """
    try:
        # Lê métricas e as expõe via Prometheus (porta 8001)
        reader = PrometheusMetricReader()
        provider = MeterProvider(metric_readers=[reader])
        metrics.set_meter_provider(provider)

        # Sobe o endpoint Prometheus
        start_http_server(port=8001)
        logger.info("📈 Servidor de métricas Prometheus iniciado na porta 8001")

        # Instrumenta FastAPI e SQLAlchemy (métricas e traces)
        FastAPIInstrumentor.instrument_app(app)
        SQLAlchemyInstrumentor().instrument(engine=engine)
        logger.info("✅ Telemetria configurada com sucesso.")
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar telemetria: {e}")
