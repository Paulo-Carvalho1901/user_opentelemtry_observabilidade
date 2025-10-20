"""
app/database.py
Configuração do SQLAlchemy (engine, SessionLocal, Base) e helpers para criar/dropar tabelas.
"""

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger(__name__)

# Use caminho relativo para garantir arquivo no diretório do projeto.
DATABASE_URL = "sqlite:///./app.db"

# Engine com check_same_thread para SQLite em multithread (uvicorn)
engine = create_engine(
    DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)

# Criar SessionLocal corretamente (corrigido autocommit typo)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa (clássica) para modelos
Base = declarative_base()

def init_db():
    """Cria as tabelas no banco (chama models para registrá-las)."""
    from . import models  # importa os modelos para registrar metadados
    logger.info("Criando tabelas...")
    Base.metadata.create_all(bind=engine)

def drop_db():
    """Remove todas as tabelas (útil para testes locais)."""
    from . import models
    logger.info("Removendo tabelas...")
    Base.metadata.drop_all(bind=engine)

# Dependência para injeção nas rotas FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
