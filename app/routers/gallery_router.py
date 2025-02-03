from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.gallery_service import GalleryService
from db.database import get_db


gallery_router = APIRouter(prefix='/api/tdim')

@gallery_router.get("/gallery")
async def get_info_for_gallery(db: AsyncSession = Depends(get_db)):
    return await GalleryService().get_all_info_gal(db)


@gallery_router.get("/gallery_pictures")
async def get_picture_for_gallery(db: AsyncSession = Depends(get_db)):
    result = await GalleryService().get_all_info_gal(db)
    paths = [f"/uploaded_files/{r['picture_path'].replace('uploaded_files/', '')}" for r in result]
    return paths