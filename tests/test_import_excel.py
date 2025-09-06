from io import BytesIO

import pandas as pd


def test_import_excel_creates_orders_and_operators(client):
    df = pd.DataFrame(
        [
            {"item": "Widget", "quantity": 2, "operator": "Alice"},
            {"item": "Gadget", "quantity": 5, "operator": "Bob"},
        ]
    )
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)

    response = client.post(
        "/orders/import-excel",
        files={
            "file": (
                "orders.xlsx",
                buffer,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        },
    )
    assert response.status_code == 200
    assert response.json()["created"] == 2

    orders_resp = client.get("/orders")
    data = orders_resp.json()
    assert len(data) == 2
    assert {o["operator"]["name"] for o in data} == {"Alice", "Bob"}


def test_import_excel_missing_required_columns(client):
    df = pd.DataFrame([{"item": "Widget"}])  # missing quantity column
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)

    response = client.post(
        "/orders/import-excel",
        files={
            "file": (
                "orders.xlsx",
                buffer,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        },
    )
    assert response.status_code == 400
    assert "Missing columns" in response.json()["detail"]
