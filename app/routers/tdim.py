from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
from services.tdim_service import TDModelService
from config import UPLOAD_DIRECTORY

tdim_router = APIRouter(prefix='/api/tdim')

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@tdim_router.post('/')
async def upload_model(file: UploadFile):
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
    files_info = await TDModelService().get_files_data()
    if not files_info:
        raise HTTPException(status_code=404, detail="No models found")
    
    # Если `files_info` это словарь, мы должны преобразовать его в список
    models = [file_info for file_info in files_info.values()]
    return models


@tdim_router.get('/{filename}')
async def get_model(filename: str):
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="application/vnd.ms-pki.stl")


@tdim_router.get('/info/{filename}')
async def get_model_info(filename: str):
    info_file = None
    files = await TDModelService().get_files_data()
    for f in files.values():
        if f["filename"] == filename:
            info_file = f
            break

    if not info_file:
        raise HTTPException(status_code=404, detail="Model info not found")
    
    return info_file
