from sqlmodel import Field, Relationship, SQLModel

from .task import Task
from .users import User


class Project(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    user_id: int | None = Field(
        foreign_key="User.id"
    )  # Foreign Key apuntando al modelo User.id y a su id
    name: str = Field(unique=True, min_length=3)
    description: str | None = Field(default=None)
    user: "User" = Relationship(
        "projects"
    )  # Para que la relación sea "bidireccional" user debe avisarle a SQLModel que él es el "otro lado" de esa conversación, es decir que el user de la tabla project haga relacion con projects y projects en la tabla user haga relacion con user
    tasks: list["Task"] = Relationship(
        "project"
    )  # un proyecto tiene muchas tareas. Aquí es donde sí necesitamos la lista: tasks: List["Task"].
