'''
There is data schemes for work with 3D-models in the project. 
'''
from pydantic import BaseModel
from datetime import datetime, date
from fastapi import UploadFile, File
from typing import BinaryIO
from typing import Optional


class TdimSchemeUpld(BaseModel):
    filename: Optional[str]
    prewiev_picture: Optional[UploadFile]
    td_file: UploadFile
    desc: Optional[str]


class TdimSchemeDB(BaseModel):
    filename: Optional[str]
    prewiev_picture: Optional[str]
    desc: str
    filepath: str
    size: int
    upload_date: date


class TdimSchemeShowList(BaseModel):
    name: str
    desc: str
    prewiev_picture: Optional[UploadFile]
    td_file: Optional[UploadFile]
    size: int
    upload_date: date