from pathlib import Path

from sqlalchemy import (
    Engine,
    event,
)
from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    sessionmaker,
)

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "app.db"

engine = create_engine(
    f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False}
)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
