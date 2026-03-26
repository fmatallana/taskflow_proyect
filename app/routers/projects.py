from fastapi import APIRouter, HTTPException, status

# 🔵 IMPORTACIONES ABSOLUTAS (app.xxx)
# Cambio de importaciones relativas (from ..db import) a absolutas para evitar circular imports
from app.database import Sessiondep
from app.models.projects import Project, ProjectBase, ProjectCreate

router = APIRouter(prefix="/projects", tags=["Project"])


@router.post(
    "/user/{user_id}", response_model=Project, status_code=status.HTTP_201_CREATED
)
async def create_project(
    project_data: ProjectCreate, session: Sessiondep, user_id: int
):
    dic_data = project_data.model_dump()
    dic_data["user_id"] = user_id
    project = Project.model_validate(dic_data)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.get("/{project_id}", response_model=ProjectBase)
async def get_project(project_id: int, session: Sessiondep):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code=404, detail=f"No hay prouyectos con el id {project_id}"
        )
    return project
