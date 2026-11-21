"""Database engine and the per-request unit of work (ADR-002 rule 5).

The engine is created lazily so tests and the OpenAPI export do not need a database.
Modules never commit on their own: `get_session` commits once after the route returns, or
rolls back if anything raised, so cross-module flows (return + rule engine) are atomic.
"""

from collections.abc import Iterator
from functools import lru_cache

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.shared.config import get_settings


class Base(DeclarativeBase):
    """Base class for every module's ORM models (`<module>/models.py`)."""


@lru_cache
def get_engine() -> Engine:
    # A short connect timeout keeps the readiness check fast when the database is down.
    return create_engine(get_settings().database_url, pool_pre_ping=True, connect_args={"connect_timeout": 3})


@lru_cache
def _session_factory() -> sessionmaker[Session]:
    return sessionmaker(bind=get_engine(), expire_on_commit=False)


def get_session() -> Iterator[Session]:
    """FastAPI dependency: one session and one transaction per request."""
    session = _session_factory()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def database_is_ready() -> bool:
    """Used by the readiness endpoint (NFR-OPS-05)."""
    try:
        with get_engine().connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
