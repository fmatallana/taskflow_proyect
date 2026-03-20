from typing import List

from sqlmodel import Field, Relationship, SQLModel

from .projects import Project


class User(SQLModel, table=True):
    id: int | None = Field(
        primary_key=True
    )  # default=None en el ID. Esto le dice a SQLModel (y a la base de datos) que cuando creas un objeto nuevo en Python, el ID empieza vacío, pero la base de datos lo generará automáticamente al guardar.
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    hashed_password: str
    projects: List["Project"] = Relationship(back_populates="user")
