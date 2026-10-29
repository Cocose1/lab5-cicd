import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app


@pytest.fixture
async def client():
    """HTTP-клиент без запуска реального сервера."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


# --- готовый пример из репозитория ---
async def test_get_existed_user(client):
    response = await client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


# --- реализованные тесты ---
async def test_create_user(client):
    """Создание пользователя: 201 и возврат созданной записи."""
    payload = {"name": "Test User", "email": "test@example.com"}
    response = await client.post("/users", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == payload["name"]
    assert body["email"] == payload["email"]
    assert "id" in body


async def test_get_not_existed_user(client):
    """Несуществующий пользователь: 404."""
    response = await client.get("/users/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


async def test_update_user(client):
    """Обновление пользователя: 200 и новые значения полей."""
    created = (await client.post("/users", json={"name": "Old", "email": "old@example.com"})).json()
    response = await client.put(f"/users/{created['id']}", json={"name": "New", "email": "new@example.com"})
    assert response.status_code == 200
    assert response.json() == {"id": created["id"], "name": "New", "email": "new@example.com"}


async def test_delete_user(client):
    """Удаление пользователя: 204, повторное получение — 404."""
    created = (await client.post("/users", json={"name": "ToDelete", "email": "del@example.com"})).json()
    response = await client.delete(f"/users/{created['id']}")
    assert response.status_code == 204
    assert (await client.get(f"/users/{created['id']}")).status_code == 404
