import os
import sys
from pathlib import Path
import json as jsonlib
import uuid

# Ensure project root is on PYTHONPATH before importing local plugins
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest_asyncio

pytest_plugins = ("pytest_asyncio",)

TEST_DB = "test.db"

os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"

from app.main import app  # noqa: E402  (import after setting env)
from app.database import Base, engine  # noqa: E402


class Response:
    def __init__(self, status_code: int, body: bytes):
        self.status_code = status_code
        self._body = body

    def json(self):
        return jsonlib.loads(self._body.decode())


class AsyncClient:
    def __init__(self, app):
        self.app = app

    async def _request(self, method: str, path: str, body: bytes = b"", headers=None):
        headers = headers or []
        sent = []

        async def receive():
            return {"type": "http.request", "body": body, "more_body": False}

        async def send(message):
            sent.append(message)

        scope = {
            "type": "http",
            "asgi": {"version": "3.0"},
            "method": method.upper(),
            "path": path,
            "raw_path": path.encode(),
            "query_string": b"",
            "headers": headers,
            "server": ("testserver", 80),
            "client": ("testclient", 50000),
        }

        await self.app(scope, receive, send)

        status = next(m["status"] for m in sent if m["type"] == "http.response.start")
        body_bytes = b"".join(m.get("body", b"") for m in sent if m["type"] == "http.response.body")
        return Response(status, body_bytes)

    async def get(self, path: str):
        return await self._request("GET", path)

    async def post(self, path: str, json=None, files=None):
        if json is not None:
            body = jsonlib.dumps(json).encode()
            headers = [(b"content-type", b"application/json")]
        elif files:
            field, (filename, fileobj, content_type) = next(iter(files.items()))
            boundary = uuid.uuid4().hex
            headers = [
                (
                    b"content-type",
                    f"multipart/form-data; boundary={boundary}".encode(),
                )
            ]
            file_content = fileobj.read()
            parts = [
                f"--{boundary}\r\n".encode(),
                f'Content-Disposition: form-data; name="{field}"; filename="{filename}"\r\n'.encode(),
                f"Content-Type: {content_type}\r\n\r\n".encode(),
                file_content,
                b"\r\n",
                f"--{boundary}--\r\n".encode(),
            ]
            body = b"".join(parts)
        else:
            body = b""
            headers = []
        return await self._request("POST", path, body, headers)

    async def put(self, path: str, json=None):
        body = jsonlib.dumps(json).encode() if json is not None else b""
        headers = [(b"content-type", b"application/json")] if json is not None else []
        return await self._request("PUT", path, body, headers)

    async def delete(self, path: str):
        return await self._request("DELETE", path)


@pytest_asyncio.fixture()
def client():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    Base.metadata.create_all(bind=engine)
    client = AsyncClient(app)
    try:
        yield client
    finally:
        engine.dispose()
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
