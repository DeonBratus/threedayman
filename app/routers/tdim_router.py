from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
import os

from db.database import get_db
from services.tdim_service import TdimService
from services.gallery_service import GalleryService
from schemes.tdim_scheme import TdimSchemeUpld, TdimSchemeUpdate
from config import UPLOAD_DIRECTORY


tdim_router = APIRouter(prefix='/api/tdim')

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@tdim_router.post('/')
async def upload_tdim(
    td_model: Annotated[TdimSchemeUpld,
    Depends()], db: AsyncSession = Depends(get_db
    )):

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


@tdim_router.get("/model_viewer")
async def get_tdimodel(
    model_id,
    db: AsyncSession = Depends(get_db)
    ):
    model_data = await TdimService().get_tdim_model(model_id=model_id, db=db)
    model_data[0].filepath
    return FileResponse(path=f"{model_data[0].filepath}", media_type="application/vnd.ms-pki.stl")


@tdim_router.get("/model_viewer/info")
async def get_data_about_tdim(model_id, db: AsyncSession = Depends(get_db)):
    model_data = await TdimService().get_tdim_model(model_id=model_id, db=db)
    return {"Filename": model_data[0].filename,
            "Size": model_data[0].file_size,
            "Format": "STL", 
            "Description": model_data[0].description,
            "Uploaded_date": model_data[0].date_upload,
    }


@tdim_router.put("/edit")
async def edit_data_model(
    td_model: Annotated[TdimSchemeUpdate, Depends()],
    db: AsyncSession = Depends(get_db)
    ):

    tdim_service = TdimService()
    res = await tdim_service.edit_model(td_model, db)
    return {"msg": f"{res}"}


@tdim_router.post("/update_version")
async def version_update():
    ...


@tdim_router.delete("/remove")
async def remove_model(model_id, db: AsyncSession = Depends(get_db)):
    tdim_service = TdimService()
    res = await tdim_service.remove_model(model_id, db)
    return res

