import pytest

pytestmark = pytest.mark.asyncio


async def test_create_order(client):
    response = await client.post("/orders/", json={"item": "Widget", "quantity": 3})
    assert response.status_code == 201
    data = response.json()
    assert data["item"] == "Widget"
    assert data["quantity"] == 3


async def test_read_orders_returns_all_orders(client):
    await client.post("/orders/", json={"item": "Widget", "quantity": 3})
    await client.post("/orders/", json={"item": "Gadget", "quantity": 5})

    response = await client.get("/orders/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert {order["item"] for order in data} == {"Widget", "Gadget"}


async def test_read_order_by_id(client):
    created = (await client.post("/orders/", json={"item": "Widget", "quantity": 3})).json()
    order_id = created["id"]

    response = await client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["item"] == "Widget"


async def test_update_order(client):
    created = (await client.post("/orders/", json={"item": "Widget", "quantity": 3})).json()
    order_id = created["id"]

    response = await client.put(
        f"/orders/{order_id}", json={"item": "Gadget", "quantity": 5}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["item"] == "Gadget"
    assert data["quantity"] == 5


async def test_delete_order(client):
    created = (await client.post("/orders/", json={"item": "Widget", "quantity": 3})).json()
    order_id = created["id"]

    response = await client.delete(f"/orders/{order_id}")
    assert response.status_code == 204

    response = await client.get(f"/orders/{order_id}")
    assert response.status_code == 404
