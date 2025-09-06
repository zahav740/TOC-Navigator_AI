import io

import pandas as pd
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_order_crud():
    resp = client.post("/orders/", json={"item": "Widget", "quantity": 2})
    assert resp.status_code == 201
    order_id = resp.json()["id"]

    resp = client.get("/orders/")
    assert resp.status_code == 200
    assert any(o["id"] == order_id for o in resp.json())

    resp = client.put(f"/orders/{order_id}", json={"quantity": 5})
    assert resp.status_code == 200
    assert resp.json()["quantity"] == 5

    resp = client.delete(f"/orders/{order_id}")
    assert resp.status_code == 204


def test_import_excel():
    df = pd.DataFrame([{ "item": "Sprocket", "quantity": 3 }])
    stream = io.BytesIO()
    df.to_excel(stream, index=False)
    stream.seek(0)
    files = {
        "file": (
            "orders.xlsx",
            stream.read(),
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    }
    resp = client.post("/orders/import-excel", files=files)
    assert resp.status_code == 201
    assert resp.json()["inserted"] == 1
