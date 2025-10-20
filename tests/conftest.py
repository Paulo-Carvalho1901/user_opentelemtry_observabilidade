# tests/conftest.py
import os
import tempfile
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from fastapi.testclient import TestClient
from app.app import app

# Cria arquivo temporário para o banco
db_fd, db_path = tempfile.mkstemp(prefix="test_db_", suffix=".sqlite")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria todas as tabelas
Base.metadata.create_all(bind=engine)

# Override da dependência get_db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def cleanup_temp_db():
    """Remove o arquivo de banco ao final dos testes."""
    yield
    os.close(db_fd)
    os.remove(db_path)

@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c
