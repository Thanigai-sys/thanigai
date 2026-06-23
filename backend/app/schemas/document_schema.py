from pydantic import BaseModel
from datetime import datetime


class DocumentResponse(BaseModel):
    id: int
    project_id: int
    file_name: str
    file_path: str
    status: str
    uploaded_at: datetime

    class Config:
        from_attributes = True