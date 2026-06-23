import os
import shutil

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Form
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.services.document_service import create_document
from app.schemas.document_schema import DocumentResponse

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post(
    "/upload",
    response_model=DocumentResponse
)
def upload_document(
    project_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    upload_dir = f"uploads/project_{project_id}"

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    file_path = os.path.join(
        upload_dir,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    document = create_document(
        db=db,
        project_id=project_id,
        file_name=file.filename,
        file_path=file_path
    )

    return document