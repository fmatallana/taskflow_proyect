from sqlmodel import Field, Relationship, SQLModel

from .projects import Project


class Task(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    title: str = Field(min_length=3)
    status: str = Field(default="pending")
    project_id: int = Field(foreign_key="Project.id")
    project: "Project" = Relationship(
        back_populates="tasks"
    )  # como una tarea solo pertenece a un proyecto se tipa project como un objeto unico
