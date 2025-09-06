import os
import pytest
from fastapi.testclient import TestClient

TEST_DB = "test.db"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"

from app.main import app  # noqa: E402  (import after setting env)
from app.database import Base, engine  # noqa: E402


@pytest.fixture()
def client():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as client:
        yield client
    engine.dispose()
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
