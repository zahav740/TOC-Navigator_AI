import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

TEST_DB = "test.db"

# Ensure project root is on PYTHONPATH for `import app`
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"

from app.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402  (import after setting env)


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
