from sqlalchemy import Column, String, Integer, UUID, Date
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()


class TdimFiles(Base):
    __tablename__ = "tdim_files"

    file_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False, unique=True)
    file_size = Column(Integer, nullable=False)
    date_upload = Column(Date, nullable=False)

    model_id = Column(String, nullable=True, default="default_model")
    model_version = Column(Integer, nullable=False, default=0)

    def to_dict(self):
        return {
            "file_id": str(self.file_id),
            "filename": self.filename,
            "filepath": self.filepath,
            "description": self.description,
            "picture_path": self.picture_path,
            "file_size": self.file_size,
            "date_upload": self.date_upload.isoformat(),
            "model_id": str(self.model_id),
        }


class GlobalModel(Base):
    __tablename__ = "models"
    model_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    modelname = Column(String, nullable=False)
    model_dirpath = Column(String, nullable=False)

    picture_path = Column(String, nullable=True)

    description = Column(String, nullable=True) # -> markdown md
    date_upload = Column(Date, nullable=False)

    current_version = Column(Integer, nullable=False, default=0)
    
    project_id = Column(UUID(as_uuid=True))


class ProjModel(Base):
    __tablename__ = "projects"

    proj_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    projname = Column(String, nullable=False, unique=True)
    picture_path = Column(String, nullable=True, unique=True)

    def to_dict(self):
        return {
            "proj_id": str(self.proj_id),
            "projname": self.projname,
            "picture_path": self.picture_path,
        }