import os
from io import BytesIO

import pandas as pd
from fastapi.testclient import TestClient

# Use a temporary SQLite database for tests
TEST_DB = "test.db"
if os.path.exists(TEST_DB):
    os.remove(TEST_DB)
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"

from app.main import app  # noqa: E402  (import after setting env)
from app.database import Base, engine  # noqa: E402

Base.metadata.create_all(bind=engine)
client = TestClient(app)


def test_import_excel_creates_orders_and_operators():
    df = pd.DataFrame([
        {"item": "Widget", "quantity": 2, "operator": "Alice"},
        {"item": "Gadget", "quantity": 5, "operator": "Bob"},
    ])
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
