"""Application configuration utilities.

This module provides a small settings helper that reads required connection
strings from environment variables.  It avoids heavy dependencies such as
`pydantic-settings` so the test environment can import it without needing
additional packages.

The expected environment variables are:

```
DATABASE_URL  # SQLAlchemy connection string
REDIS_URL     # Redis connection string
QDRANT_URL    # Qdrant vector DB endpoint
```

If a variable is not set a sensible default pointing at local services is
used instead.  A ``.env`` file, when present, is loaded via ``python-dotenv``
before values are read.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Load variables from a local .env file if available.  This is a best effort;
# missing files or the python-dotenv package simply result in environment
# defaults being used.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")


@dataclass
class Settings:
    database_url: str = os.getenv(
        "DATABASE_URL", "postgresql://toc_ai:magarel@localhost:5432/toc_ai"
    )
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    qdrant_url: str = os.getenv("QDRANT_URL", "http://qdrant:6333")


settings = Settings()
