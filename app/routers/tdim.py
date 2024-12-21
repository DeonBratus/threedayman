from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from config import UPLOAD_DIRECTORY
from services.tdim_service import TDModelService
import os

# There is endpoint for all project


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


@tdim_router.get('/{filename}')
async def get_model(filename: str):
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="application/vnd.ms-pki.stl")