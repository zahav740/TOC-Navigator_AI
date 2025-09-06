import os
from typing import List
from uuid import uuid4

try:  # pragma: no cover - optional dependency
    from qdrant_client import QdrantClient, models
except Exception:  # pragma: no cover - package may be unavailable
    QdrantClient = None  # type: ignore
    models = None  # type: ignore

COLLECTION_NAME = "order-events"
VECTOR_SIZE = 3


def _client() -> QdrantClient:
    """Create a Qdrant client using env variables."""
    host = os.getenv("QDRANT_HOST", "qdrant")
    port = int(os.getenv("QDRANT_PORT", "6333"))
    return QdrantClient(host=host, port=port)


def _ensure_collection(client: QdrantClient) -> None:
    """Ensure the collection exists."""
    try:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE),
        )
    except Exception:
        # Collection might already exist; ignore errors
        pass


def _embed(text: str) -> List[float]:
    """Naive text embedding.

    This placeholder simply converts the first characters to floats. It keeps the
    implementation lightweight and deterministic for tests while providing a
    reasonable stub for future replacement with a real embedding model.
    """
    vector = [float(ord(c)) / 255.0 for c in text[:VECTOR_SIZE]]
    vector += [0.0] * (VECTOR_SIZE - len(vector))
    return vector


def log_event(order_id: int, text: str) -> None:
    """Store an event in Qdrant linked to an order.

    If the optional `qdrant_client` dependency is not installed the function
    becomes a no-op so the rest of the application and tests can run without
    external services.
    """

    if QdrantClient is None:  # pragma: no cover - dependency missing
        return

    client = _client()
    _ensure_collection(client)
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            models.PointStruct(
                id=uuid4().int >> 64,
                vector=_embed(text),
                payload={"order_id": order_id, "text": text},
            )
        ],
    )
