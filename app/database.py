"""
app/database_refatorado.py
Configuração do SQLAlchemy e helpers de inicialização.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ---------------------------------------------------------------
# Configuração do banco de dados
# ---------------------------------------------------------------
DATABASE_URL = "sqlite:///./app.db"

# O parâmetro check_same_thread é necessário apenas para SQLite + FastAPI
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False  # defina True se quiser logs SQL no console (modo dev)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ---------------------------------------------------------------
# Inicialização e limpeza do banco
# ---------------------------------------------------------------
def init_db():
    """Cria todas as tabelas do banco de dados."""
    from . import models
    Base.metadata.create_all(bind=engine)

def drop_db():
    """Remove todas as tabelas do banco de dados."""
    from . import models
    Base.metadata.drop_all(bind=engine)

# ---------------------------------------------------------------
# Dependência para FastAPI
# ---------------------------------------------------------------
def get_db():
    """Cria e fecha a sessão do banco de dados automaticamente."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
