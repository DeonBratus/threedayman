from sqlalchemy import Column, String, Integer, Boolean, UUID, Date
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()


class TdimModel(Base):
    __tablename__ = "tdim_files"

    file_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    picture_path = Column(String, nullable=True)
    file_size = Column(Integer, nullable=False)
    date_upload = Column(Date, nullable=False)