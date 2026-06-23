from app.database.db import engine

from app.database.models import Project
from app.database.document_model import Document

from app.database.db import Base

Base.metadata.create_all(bind=engine)

print("Tables Created Successfully")