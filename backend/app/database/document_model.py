from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from datetime import datetime

from app.database.db import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id")
    )

    file_name = Column(
        String(255),
        nullable=False
    )

    file_path = Column(
        String(500),
        nullable=False
    )

    status = Column(
        String(50),
        default="UPLOADED"
    )

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow
    )