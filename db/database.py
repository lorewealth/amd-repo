from sqlalchemy import Engine, event
from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.config import get_settings

settings = get_settings()


engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
