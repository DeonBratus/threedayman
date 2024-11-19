from fastapi import APIRouter, UploadFile, File, HTTPException
from config import UPLOAD_DIRECTORY
from services.tdim_service import TDModelService
import os

tdim_router = APIRouter(prefix='/api/tdim')

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@tdim_router.post('/')
async def load_model(file: UploadFile):
    file_msg, ok = await TDModelService().upload_file(
        file=file.file,
        filename=file.filename
    )
    if not ok:
        raise HTTPException(
            status_code=400,
            detail=file_msg)
    return file_msg


@tdim_router.get('/')
async def get_models_list():
    files_info = await TDModelService().get_file_info()
    return files_info
