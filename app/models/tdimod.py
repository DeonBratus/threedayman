from pydantic import BaseModel
from datetime import datetime, date
from fastapi import UploadFile
from typing import Optional

class TDIModel(BaseModel):
    filename: Optional[str]
    prewiev_picture: Optional[UploadFile]
    td_file: UploadFile
    desc: Optional[str] = None


class TDIModelDB(TDIModel):
    size: int
    upload_date: date

'''
data = {
    name: str,
    date_upload: date
    date_update: date
    size: Mb
    description: str,
    histories: ?,
    depends: ?
}
'''