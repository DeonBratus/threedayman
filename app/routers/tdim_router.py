from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import os
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from db.database import get_db
from services.tdim_service import TdimService
from services.gallery_service import GalleryService
from schemes.tdim_scheme import TdimSchemeUpld
from config import UPLOAD_DIRECTORY

tdim_router = APIRouter(prefix='/api/tdim')

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@tdim_router.post('/')
async def upload_model(
    td_model: Annotated[TdimSchemeUpld, Depends()],
    db: AsyncSession = Depends(get_db),
    ):
    # split info and file
    tdiminfo = {
        "filename": td_model.filename,
        "desc": td_model.desc,
        "raw_filename": td_model.td_file.filename,
        "picture_path": td_model.prewiev_picture.filename,
        "proj_name": td_model.proj_name
    }

    file_msg, ok = await TdimService().upload_new_tdim(
        file=td_model.td_file.file,
        data=tdiminfo, 
        db=db
    )

    await GalleryService().upload_preview_picture(
        td_model.prewiev_picture.file,
        td_model.filename,
        td_model.prewiev_picture.filename)

    if not ok:
        raise HTTPException(
            status_code=400,
            detail=file_msg)
    
    return tdiminfo


@tdim_router.get("/gallery")
async def get_info_for_gallery(db: AsyncSession = Depends(get_db)):
    return await GalleryService().get_all_info_gal(db)


@tdim_router.get("/gallery_pictures")
async def get_picture_for_gallery(db: AsyncSession = Depends(get_db)):
    result = await GalleryService().get_all_info_gal(db)
    paths = [f"/uploaded_files/{r['picture_path'].replace('uploaded_files/', '')}" for r in result]
    return paths


@tdim_router.get("/model_viewer")
async def get_model(model_id, db: AsyncSession = Depends(get_db)):
    model_data = await TdimService().get_tdimfile(model_id=model_id, db=db)
    model_data[0].filepath
    return FileResponse(path=f"{model_data[0].filepath}", media_type="application/vnd.ms-pki.stl")


@tdim_router.get("/model_viewer/info")
async def get_info_model(model_id, db: AsyncSession = Depends(get_db)):
    model_data = await TdimService().get_tdimfile(model_id=model_id, db=db)
    return {"Filename": model_data[0].filename,
            "Size": model_data[0].file_size,
            "Format": "STL", 
            "Description": model_data[0].description,
            "Uploaded_date": model_data[0].date_upload,
                }

@tdim_router.delete("/remove")
async def remove_model(model_id, db: AsyncSession = Depends(get_db)):
    tdim_service = TdimService()
    res = await tdim_service.remove_model(model_id, db)
    return res


@tdim_router.post("/update")
async def update_model():
    ...


@tdim_router.post("/update_version")
async def version_update():
    ...

    