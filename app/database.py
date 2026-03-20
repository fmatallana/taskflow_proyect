from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Session, SQLModel, create_engine

sqlite_name = "taskflow.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"

engine = create_engine(sqlite_url, echo=True)  # echo=True te muestra el SQL en consola


def create_db_and_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


def get_session():
    with Session(engine) as session:
        yield session


Sessiondep = Annotated[Session, Depends(get_session)]
