from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
import os
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from db.database import get_db
from services.project_service import ProjectService

proj_api = APIRouter(prefix="/api/proj")


@proj_api.post("/")
async def create_project(projname: str, pic: UploadFile, db: AsyncSession = Depends(get_db)):
    proj_service = ProjectService()
    res = await proj_service.create_proj(
        data={"proj_name":projname},
        pic=pic.file, 
        picname=pic.filename,
        db=db)
    return res