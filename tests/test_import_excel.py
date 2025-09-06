from io import BytesIO

import pandas as pd
import pytest

pytestmark = pytest.mark.asyncio


async def test_import_excel_creates_orders(client):
    df = pd.DataFrame(
        [
            {
                "client": "ACME",
                "date": "2023-01-01",
                "status": "new",
                "manager": "Alice",
            },
            {
                "client": "Globex",
                "date": "2023-01-02",
                "status": "done",
                "manager": "Bob",
            },
        ]
    )
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)

    response = await client.post(
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
    body = response.json()
    assert body["created"] == 2
    assert body["errors"] == []

    orders_resp = await client.get("/orders/")
    data = orders_resp.json()
    assert len(data) == 2
    assert {o["client"] for o in data} == {"ACME", "Globex"}


async def test_import_excel_missing_required_columns(client):
    df = pd.DataFrame([{"client": "ACME"}])  # missing other required columns
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)

    response = await client.post(
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
