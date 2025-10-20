# tests/conftest.py
import os
import time
import tempfile
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from fastapi.testclient import TestClient
from app.app import app

# ============================================================
# 🧱 Configuração do banco de dados temporário para testes
# ============================================================

# Cria um arquivo SQLite temporário
db_fd, db_path = tempfile.mkstemp(prefix="test_db_", suffix=".sqlite")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

# Cria engine e sessão de teste
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria todas as tabelas no banco de teste
Base.metadata.create_all(bind=engine)

# ============================================================
# 🔄 Override da dependência get_db (usado pelo FastAPI)
# ============================================================
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# ============================================================
# 🧹 Limpeza do banco de teste ao final da sessão
# ============================================================
@pytest.fixture(scope="session", autouse=True)
def cleanup_temp_db():
    """Fecha conexões e remove o arquivo do banco ao final dos testes."""
    yield
    try:
        # Fecha todas as conexões do SQLAlchemy
        engine.dispose()

        # Aguarda um pouco para o SQLite liberar o arquivo (necessário no Windows)
        time.sleep(0.2)

        # Fecha o descritor e remove o arquivo
        os.close(db_fd)
        os.remove(db_path)
    except PermissionError:
        # Caso o SQLite ainda esteja segurando o arquivo
        time.sleep(0.5)
        try:
            os.remove(db_path)
        except Exception:
            print(f"⚠️ Aviso: não foi possível remover o arquivo {db_path} (em uso).")
    except Exception as e:
        print(f"⚠️ Erro inesperado ao limpar o banco de testes: {e}")

# ============================================================
# 🚀 Fixture do cliente FastAPI para os testes
# ============================================================
@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c
