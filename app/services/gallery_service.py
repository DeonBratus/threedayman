import os
from typing import BinaryIO
from sqlalchemy.ext.asyncio import AsyncSession
from dals.tdim_dals import TdimDals
from config import UPLOAD_DIRECTORY


class GalleryService:
    
    async def upload_preview_picture(self, picture: BinaryIO, folder_name: str, picname: str):
        complex_path = f"{UPLOAD_DIRECTORY}/{folder_name}"
        file_path = os.path.join(complex_path, f"{picname}")

        with open(file_path, "wb") as pf:
            pf.write(picture.read())
        
        return {"msg": "file has been uploaded"}


    async def get_all_info_gal(self, db: AsyncSession):
        async with db as session:
            tdim_dals = TdimDals(session)
            res = await tdim_dals.get_datapics_gallery()
            return res
    
    
    async def get_tdim_info_gal(self, db: AsyncSession):
        async with db as session:
            tdim_dals = TdimDals(session)
            res = await tdim_dals.get_datatdim_gallery()
            return res