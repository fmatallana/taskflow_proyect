from fastapi import APIRouter, status

from .db import Sessiondep
from .models import Project, ProjectCreate

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
