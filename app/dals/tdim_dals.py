#Database access layer for work with database aka repository
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, and_, select, delete

from schemes.tdim_scheme import TdimSchemeUpdate
from app.models.db_model import TdimFiles
from sqlalchemy.exc import NoResultFound

class TdimDals:
    
    def __init__(self, db_session: AsyncSession):
        self.db_session: AsyncSession = db_session

    
    async def upload_file(self, tdim_data: dict) -> TdimFiles:
        
        up_file = TdimFiles (
            filename=tdim_data["filename"],
            filepath=tdim_data["filepath"],
            file_size=tdim_data["size"],
            description=tdim_data["desc"],
            date_upload=tdim_data["upload_date"],
            picture_path=tdim_data["picture_path"],
            proj_name=tdim_data["proj_name"]
        )

        self.db_session.add(up_file)
        await self.db_session.flush()
        return up_file
    
    
    async def get_datapics_gallery(self) -> List[dict]:
        """Получение всех файлов из базы данных."""
        try:
            query = select(
                TdimFiles.file_id,
                TdimFiles.filename,
                TdimFiles.picture_path,
                TdimFiles.date_upload
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
            TdimFiles.file_id,
            TdimFiles.filename,
            TdimFiles.filepath,
            TdimFiles.date_upload
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
        query = select(TdimFiles).where(TdimFiles.file_id == model_id)
        res = await self.db_session.execute(query)
        files_info = res.scalars().all()
        return files_info
    

    async def get_path_from_id(self, model_id):
        query = select(TdimFiles.filepath, TdimFiles.picture_path, TdimFiles.filename).where(TdimFiles.file_id == model_id)
        res = await self.db_session.execute(query)
        data = res.all()
        return {"filepath": data[0][0], "picpath": data[0][1], "filename": data[0][2]}


    async def delete_tdim(self, model_id):
        query = delete(TdimFiles).where(TdimFiles.file_id == model_id)
        res = await self.db_session.execute(query)
        await self.db_session.commit()
        return res.rowcount
    

    async def edit_tdim_data(self, tdim_data: dict):
        tdim_id = tdim_data.get("tdim_id")

        if not tdim_id:
            raise ValueError("Не указан file_id для обновления записи")

        query = select(TdimFiles).where(TdimFiles.file_id == tdim_id)
        res = await self.db_session.execute(query)
        tdim_rec = res.scalars().first()

        if not tdim_rec:
            raise NoResultFound(f"Запись с id {tdim_id} не найдена")
        
        if 'filename' in tdim_data and tdim_data['filename'] is not None:
            tdim_rec.filename = tdim_data['filename']
        if 'desc' in tdim_data and tdim_data['desc'] is not None:
            tdim_rec.description = tdim_data['desc']
        if 'proj_name' in tdim_data and tdim_data['proj_name'] is not None:
            tdim_rec.proj_name = tdim_data['proj_name']

        await self.db_session.flush()
        await self.db_session.commit()

        return tdim_rec.to_dict()


    async def reload_tdim(self, tdim_id):
        ...