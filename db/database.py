import logging
from fastapi import HTTPException, status
from sqlalchemy.exc import OperationalError
from sqlmodel import create_engine, Session, SQLModel

from db.tables.users import User

sqlite_file_name = "./db/sqlite/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

SQLModel.metadata.create_all(engine)


def get_session():
    session_engine: Session = Session(engine)
    try:
        with session_engine as session:
            yield session
    except OperationalError as e:
        logging.error(f"Database connection error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error"
        )
    finally:
        session_engine.close()
