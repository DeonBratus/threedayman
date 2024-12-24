#Database access layer for work with database aka repository
from sqlalchemy.ext.asyncio import AsyncSession
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