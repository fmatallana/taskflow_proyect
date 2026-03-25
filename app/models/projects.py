from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.tasks import Task
    from app.models.users import User


class ProjectBase(SQLModel):
    name: str = Field(unique=True, min_length=3)
    description: str | None = Field(default=None)


class Project(ProjectBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(
        foreign_key="user.id"
    )  # Foreign Key apuntando al modelo User.id y a su id
    user: "User" = Relationship(
        back_populates="projects"
    )  # Para que la relación sea "bidireccional" user debe avisarle a SQLModel que él es el "otro lado" de esa conversación, es decir que el user de la tabla project haga relacion con projects y projects en la tabla user haga relacion con user
    tasks: list["Task"] = Relationship(
        back_populates="project"
    )  # un proyecto tiene muchas tareas. Aquí es donde sí necesitamos la lista: tasks: List["Task"].


class ProjectCreate(ProjectBase):
    pass
