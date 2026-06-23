from sqlalchemy.orm import Session
from app.database.document_model import Document


def create_document(
    db: Session,
    project_id: int,
    file_name: str,
    file_path: str
):
    document = Document(
        project_id=project_id,
        file_name=file_name,
        file_path=file_path
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document