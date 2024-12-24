from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
import os
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from services.tdim_service import TdimService
from schemes.tdim_scheme import TdimSchemeUpld
from config import UPLOAD_DIRECTORY
from typing import Annotated

tdim_router = APIRouter(prefix='/api/tdim')

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@tdim_router.post('/')
async def upload_model(td_model: Annotated[TdimSchemeUpld, Depends()],  db: AsyncSession = Depends(get_db)):
    # split info and file
    tdiminfo = {
        "filename": td_model.filename,
        "desc": td_model.desc,
        "raw_filename": td_model.td_file.filename,
        "picture_path": td_model.prewiev_picture.filename
    }

    file_msg, ok = await TdimService().upload_file(
        file=td_model.td_file.file,
        data=tdiminfo, 
        db = db
    )
    await TdimService().upload_preview_picture(
        td_model.prewiev_picture.file,
        td_model.filename,
        td_model.prewiev_picture.filename)

    if not ok:
        raise HTTPException(
            status_code=400,
            detail=file_msg)
    
    return tdiminfo


@tdim_router.get('/')
async def get_models_list():
    files_info = await TdimService().get_all_datafiles()
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
    files = await TdimService().get_all_datafiles()
    for f in files.values():
        if f["filename"] == filename:
            info_file = f
            break

    if not info_file:
        raise HTTPException(status_code=404, detail="Model info not found")
    
    return info_file
