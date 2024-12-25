#Database access layer for work with database aka repository
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, and_, select
from models.tdim_dbmodel import TdimModel

class TdimDals:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    
    async def upload_file(self, tdim_info: dict) -> TdimModel:
        
        up_file = TdimModel(
            filename=tdim_info["filename"],
            filepath=tdim_info["filepath"],
            file_size=tdim_info["size"],
            description=tdim_info["desc"],
            date_upload=tdim_info["upload_date"],
            picture_path=tdim_info["picture_path"]
        )

        self.db_session.add(up_file)
        await self.db_session.flush()
        return up_file
    
    
    async def get_all_files(self) -> List[dict]:
        """Получение всех файлов из базы данных."""
        try:
            query = select(
                TdimModel.filename,
                TdimModel.picture_path,
                TdimModel.date_upload
            )
            result = await self.db_session.execute(query)
            files_info = result.all()
            return [
                {
                    "filename": file.filename,
                    "picture_path": file.picture_path,
                    "date_upload": file.date_upload
                } 
                for file in files_info
            ]
        except NameError as e:
            raise e