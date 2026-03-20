from typing import List

from sqlmodel import Field, Relationship, SQLModel

from .projects import Project


class UserBase(SQLModel):
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    projects: List["Project"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password: str  # El usuario envía "password", no "hashed_password"

    """
    UserBase: Solo tiene los datos que siempre viajan (username, email).

User (La Tabla): Hereda lo de Base, y AQUÍ es donde pones el id, el hashed_password projects: list["Project"] = Relationship(...). ¿Por qué? Porque las relaciones y los IDs solo viven dentro de la base de datos.

UserCreate: Hereda lo de Base, y le agregamos el password en texto plano.

Al separar esto, logramos que cuando el cliente se registre enviando el JSON, FastAPI valide que no nos esté intentando inyectar un id falso o proyectos que no le corresponden. El esquema UserCreate actúa como un filtro de seguridad. 🛡️
    """
