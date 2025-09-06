import pytest

pytestmark = pytest.mark.asyncio


async def test_create_operator(client):
    response = await client.post("/operators/", json={"name": "Alice"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert "id" in data


async def test_read_operators_returns_all(client):
    await client.post("/operators/", json={"name": "Alice"})
    await client.post("/operators/", json={"name": "Bob"})

    response = await client.get("/operators/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert {op["name"] for op in data} == {"Alice", "Bob"}


async def test_read_operator_by_id(client):
    created = (await client.post("/operators/", json={"name": "Alice"})).json()
    operator_id = created["id"]

    response = await client.get(f"/operators/{operator_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == operator_id
    assert data["name"] == "Alice"


async def test_update_operator(client):
    created = (await client.post("/operators/", json={"name": "Alice"})).json()
    operator_id = created["id"]

    response = await client.put(f"/operators/{operator_id}", json={"name": "Bob"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Bob"


async def test_delete_operator(client):
    created = (await client.post("/operators/", json={"name": "Alice"})).json()
    operator_id = created["id"]

    response = await client.delete(f"/operators/{operator_id}")
    assert response.status_code == 204

    response = await client.get(f"/operators/{operator_id}")
    assert response.status_code == 404
