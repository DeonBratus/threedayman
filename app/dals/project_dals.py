from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, and_, select
from models.tdim_dbmodel import ProjModel


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