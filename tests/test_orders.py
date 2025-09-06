import pytest

def test_create_order(client):
    response = client.post("/orders/", json={"item": "Widget", "quantity": 3})
    assert response.status_code == 201
    data = response.json()
    assert data["item"] == "Widget"
    assert data["quantity"] == 3


def test_read_orders_returns_all_orders(client):
    client.post("/orders/", json={"item": "Widget", "quantity": 3})
    client.post("/orders/", json={"item": "Gadget", "quantity": 5})

    response = client.get("/orders/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert {order["item"] for order in data} == {"Widget", "Gadget"}


def test_read_order_by_id(client):
    created = client.post("/orders/", json={"item": "Widget", "quantity": 3}).json()
    order_id = created["id"]

    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["item"] == "Widget"


def test_update_order(client):
    created = client.post("/orders/", json={"item": "Widget", "quantity": 3}).json()
    order_id = created["id"]

    response = client.put(
        f"/orders/{order_id}", json={"item": "Gadget", "quantity": 5}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["item"] == "Gadget"
    assert data["quantity"] == 5


def test_delete_order(client):
    created = client.post("/orders/", json={"item": "Widget", "quantity": 3}).json()
    order_id = created["id"]

    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 204

    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 404


@pytest.mark.parametrize(
    "payload,detail",
    [
        ({"item": "", "quantity": 1}, "Item is required"),
        ({"item": "Widget", "quantity": 0}, "Quantity must be positive"),
        (
            {"item": "Widget", "quantity": 1, "operator_id": 999},
            "Operator not found",
        ),
    ],
)
def test_create_order_validation_errors(client, payload, detail):
    response = client.post("/orders/", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == detail


def test_update_order_validation_errors(client):
    created = client.post("/orders/", json={"item": "Widget", "quantity": 3}).json()
    order_id = created["id"]

    response = client.put(f"/orders/{order_id}", json={"item": ""})
    assert response.status_code == 400
    assert response.json()["detail"] == "Item is required"

    response = client.put(f"/orders/{order_id}", json={"quantity": 0})
    assert response.status_code == 400
    assert response.json()["detail"] == "Quantity must be positive"

    response = client.put(f"/orders/{order_id}", json={"operator_id": 999})
    assert response.status_code == 400
    assert response.json()["detail"] == "Operator not found"


def test_delete_nonexistent_order(client):
    response = client.delete("/orders/999")
    assert response.status_code == 404
