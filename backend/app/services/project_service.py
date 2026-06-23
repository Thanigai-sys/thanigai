from sqlalchemy.orm import Session
from app.database.models import Project


def create_project(
    db: Session,
    project_name: str,
    description: str = None
):
    project = Project(
        project_name=project_name,
        description=description
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def get_projects(db: Session):
    return db.query(Project).all()


def get_project_by_id(
    db: Session,
    project_id: int
):
    return (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )