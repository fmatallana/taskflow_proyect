from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.database import Sessiondep
from app.models.tasks import Task, TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "/project/{project_id}", response_model=Task, status_code=status.HTTP_201_CREATED
)
async def create_tasks(tasks_data: TaskCreate, session: Sessiondep, project_id: int):
    tasks_data = tasks_data.model_dump()
    tasks_data["project_id"] = project_id
    tasks = Task.model_validate(tasks_data)
    session.add(tasks)
    session.commit()
    session.refresh(tasks)
    return tasks


@router.get("/project/{project_id}", response_model=list[Task])
async def get_tasks_for_project(project_id: int, session: Sessiondep):
    statement = select(Task).where(Task.project_id == project_id)
    tasks = session.exec(statement).all()
    if not tasks:
        raise HTTPException(
            status_code=404, detail=f"No hay tasks con el id {project_id}"
        )
    return tasks


@router.patch("/{task_id}", response_model=Task)
async def update_tasks(tasks_data: TaskUpdate, session: Sessiondep, task_id: int):
    tasks_db = session.get(Task, task_id)
    if not tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tasks doesn´t exist"
        )
    # RECORDATORIO: exclude_unset=True evita sobrescribir con valores Nulos lo que el usuario no envió.
    tasks_data_dict = tasks_data.model_dump(exclude_unset=True)
    tasks_db.sqlmodel_update(tasks_data_dict)
    session.add(tasks_db)
    session.commit()
    session.refresh(tasks_db)
    return tasks_db


@router.delete("/{task_id}")
async def delete_tasks(session: Sessiondep, task_id: int):
    tasks_db = session.get(Task, task_id)
    if not tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tasks doesn´t exist"
        )
    session.delete(tasks_db)
    session.commit()
    return {"detail": "ok"}
