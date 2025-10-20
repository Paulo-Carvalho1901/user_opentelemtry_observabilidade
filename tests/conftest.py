# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from fastapi.testclient import TestClient
from app.app import app

# Banco de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria todas as tabelas no banco de teste
Base.metadata.create_all(bind=engine)

# Override da dependência get_db do FastAPI
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Fixture do client FastAPI
@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c
