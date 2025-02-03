from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from db.database import get_db
from services.project_service import ProjectService


proj_api = APIRouter(prefix="/api/proj")


@proj_api.post("/")
async def create_project(projname: str, pic: Optional[UploadFile] = None, db: AsyncSession = Depends(get_db)):
    proj_service = ProjectService()
    res = await proj_service.create_proj(
        data={"proj_name":projname},
        pic=pic.file, 
        picname=pic.filename,
        db=db)
    return res


@proj_api.get('/list')
async def show_projects_list(db: AsyncSession = Depends(get_db)):
    proj_service = ProjectService()
    res = await proj_service.show_all_projs(db)
    return res 


@proj_api.get("/")
async def get_list_tdims_of_proj(proj_name, db: AsyncSession = Depends(get_db)):
    proj_service = ProjectService()
    res = await proj_service.get_tdims_from_proj(proj_name=proj_name, db=db)
    return res