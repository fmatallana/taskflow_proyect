from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.projects import Project


class TaskBase(SQLModel):
    title: str = Field(min_length=3)
    status: str = Field(default="pending")


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    project: "Project" = Relationship(
        back_populates="tasks"
    )  # como una tarea solo pertenece a un proyecto se tipa project como un objeto unico


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=3)
    status: str | None = Field(default=None)
