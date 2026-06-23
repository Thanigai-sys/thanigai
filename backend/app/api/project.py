from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.project_schema import (
    ProjectCreate,
    ProjectResponse
)
from app.services.project_service import (
    create_project,
    get_projects,
    get_project_by_id
)

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post(
    "",
    response_model=ProjectResponse
)
def create_project_api(
    request: ProjectCreate,
    db: Session = Depends(get_db)
):
    return create_project(
        db=db,
        project_name=request.project_name,
        description=request.description
    )


@router.get(
    "",
    response_model=list[ProjectResponse]
)
def get_projects_api(
    db: Session = Depends(get_db)
):
    return get_projects(db)


@router.get(
    "/{project_id}",
    response_model=ProjectResponse
)
def get_project_api(
    project_id: int,
    db: Session = Depends(get_db)
):
    return get_project_by_id(
        db,
        project_id
    )