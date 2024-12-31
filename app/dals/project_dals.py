from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, and_, select
from models.tdim_dbmodel import ProjModel
from models.tdim_dbmodel import TdimModel

class ProjDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    
    async def create_project(self, proj_data: dict) -> ProjModel:
        
        new_project = ProjModel(
            projname=proj_data["projname"],
            picture_path=proj_data["picture_path"]
        )

        self.db_session.add(new_project)
        await self.db_session.flush()
        return new_project
    

    async def get_all_projs(self):
        query = select(ProjModel)
        result = await self.db_session.execute(query)
        data = result.scalars().all()
        return data        


    async def get_tdims_from_proj(self, proj_name):
        query = select(TdimModel).where(proj_name == TdimModel.proj_name)
        res = await self.db_session.execute(query)
        data = res.scalars().all()
        return data
