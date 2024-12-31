#Database access layer for work with database aka repository
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, and_, select
from models.tdim_dbmodel import TdimModel

class TdimDals:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    
    async def upload_file(self, tdim_info: dict) -> TdimModel:
        
        up_file = TdimModel (
            filename=tdim_info["filename"],
            filepath=tdim_info["filepath"],
            file_size=tdim_info["size"],
            description=tdim_info["desc"],
            date_upload=tdim_info["upload_date"],
            picture_path=tdim_info["picture_path"],
            proj_name=tdim_info["proj_name"]
        )

        self.db_session.add(up_file)
        await self.db_session.flush()
        return up_file
    
    
    async def get_datapics_gallery(self) -> List[dict]:
        """Получение всех файлов из базы данных."""
        try:
            query = select(
                TdimModel.file_id,
                TdimModel.filename,
                TdimModel.picture_path,
                TdimModel.date_upload
            )
            result = await self.db_session.execute(query)
            files_info = result.all()
            return [
                {
                    "file_id": file.file_id,
                    "filename": file.filename,
                    "picture_path": file.picture_path,
                    "date_upload": file.date_upload
                } 
                for file in files_info
            ]
        except NameError as e:
            raise e
        

    async def get_datatdim_gallery(self) -> List[dict]:
        query = select(
            TdimModel.file_id,
            TdimModel.filename,
            TdimModel.filepath,
            TdimModel.date_upload
        )
        res = await self.db_session.execute(query)
        res_info = res.all()
        return [
            {
            "file_id": info.file_id,
            "filename": info.filename,
            "filepath": info.filepath,
            "date_upload": info.date_upload
            }
        for info in res_info
        ]



    async def get_data_for_viewer(self, model_id):
        query = select(TdimModel).where(TdimModel.file_id == model_id)
        res = await self.db_session.execute(query)
        files_info = res.scalars().all()
        return files_info