# tests/test_users.py
import pytest
from fastapi.testclient import TestClient
from app.schemas import PessoaSchemaIn

@pytest.mark.order(1)
def test_create_user(client: TestClient):
    payload = {
        "nome": "Alice",
        "email": "alice@example.com",
        "senha": "1234",
        "cidade": "SBO",
        "activo": True
    }
    response = client.post("/pessoas/create", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert data["cidade"] == "SBO"
    assert data["activo"] is True
    assert "id" in data


@pytest.mark.order(2)
def test_create_user_duplicate_email(client: TestClient):
    """Tenta criar usuário com e-mail duplicado"""
    payload = {
        "nome": "Alice Dup",
        "email": "alice@example.com",  # mesmo e-mail do anterior
        "senha": "abcd",
        "cidade": "SBO",
        "activo": True
    }
    response = client.post("/pessoas/create", json=payload)
    assert response.status_code == 400

    # ✅ aceita diferentes mensagens de erro (flexível)
    detail = response.json().get("detail", "").lower()
    assert "duplicado" in detail or "já existe" in detail


@pytest.mark.order(3)
def test_list_users(client: TestClient):
    """Lista todos os usuários"""
    response = client.get("/pessoas/all")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(user["email"] == "alice@example.com" for user in data)


@pytest.mark.order(4)
def test_get_user_by_id(client: TestClient):
    """Busca usuário pelo ID"""
    response = client.get("/pessoas/all")
    user_id = response.json()[0]["id"]

    response = client.get(f"/pessoas/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["nome"] == "Alice"
