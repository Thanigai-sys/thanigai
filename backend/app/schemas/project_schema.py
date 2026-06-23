from pydantic import BaseModel
from datetime import datetime


class ProjectCreate(BaseModel):
    project_name: str
    description: str | None = None


class ProjectResponse(BaseModel):
    id: int
    project_name: str
    description: str | None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True