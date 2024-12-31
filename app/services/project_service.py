import os
from sqlalchemy.ext.asyncio import AsyncSession
from typing import BinaryIO
from config import UPLOAD_DIRECTORY
from dals.project_dals import ProjDAL

class ProjectService:
    
    async def create_proj(self, data: dict, pic: BinaryIO, picname, db: AsyncSession):
        proj_path = f"{UPLOAD_DIRECTORY}/{data['proj_name']}"
        os.makedirs(proj_path, exist_ok=True)
        msg = await self.upload_preview_picture(picture=pic,
                                    path=proj_path,
                                    picname=f"_preview_project__{picname}")
        async with db as session:
            async with session.begin():
                proj_dal = ProjDAL(db_session=session)
                await proj_dal.create_project(proj_data={"projname": data['proj_name'], "picture_path": msg['path']})
        return msg
    

    async def upload_preview_picture(self, picture: BinaryIO, path: str, picname: str):
        file_path = os.path.join(path, f"{picname}")

        with open(f"{file_path}", "wb") as pf:
            pf.write(picture.read())
        
        return {"msg": "file has been uploaded", "path": file_path}
