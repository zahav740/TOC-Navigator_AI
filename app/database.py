"""Database configuration and helpers.

This module centralises creation of the SQLAlchemy engine and session as well as
helpers for running Alembic migrations.  It aims to provide a sensible default
configuration that works for both development (SQLite) and production (PostgreSQL
by default) while enabling connection pooling and `pool_pre_ping` for robustness.
"""

import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings

# ---------------------------------------------------------------------------
# Engine & Session configuration
# ---------------------------------------------------------------------------

DATABASE_URL = settings.database_url

if DATABASE_URL.startswith("sqlite"):
    # SQLite needs special arguments and doesn't really benefit from pooling.
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
    )
else:
    # Basic connection pooling for production databases.
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=int(os.getenv("DB_POOL_SIZE", 5)),
        max_overflow=int(os.getenv("DB_MAX_OVERFLOW", 10)),
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Provide a transactional scope around a series of operations."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Alembic helpers
# ---------------------------------------------------------------------------


def run_migrations() -> None:
    """Run Alembic migrations to ensure the database schema is up to date."""

    from alembic import command
    from alembic.config import Config

    config_path = Path(__file__).resolve().parents[1] / "alembic.ini"
    alembic_cfg = Config(str(config_path))
    command.upgrade(alembic_cfg, "head")


def init_db() -> None:
    """Initialise database by running migrations."""

    # In tests using SQLite we may not have migrations; falling back to create_all
    try:
        run_migrations()
    except Exception:  # pragma: no cover - best effort
        Base.metadata.create_all(bind=engine)
