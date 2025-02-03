import os
from typing import BinaryIO
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from config import UPLOAD_DIRECTORY
from dals.tdim_dals import TdimDals

'''
Services of 3d-project. This service for only manage files
There is logic of managment files only.
CRUD --> UGERD
'''

class TdimService:

    async def upload_new_tdim(self, file: BinaryIO, data: dict, db: AsyncSession) -> dict | bool:
        complex_path = f"{UPLOAD_DIRECTORY}/{data["filename"]}"
        os.makedirs(complex_path, exist_ok=True)
        try:
            file_path = os.path.join(complex_path, data["raw_filename"])
            msg, ok = await self.__file_existing_check(filename=data["raw_filename"], name=data["filename"])
            if not ok: 
                return msg, ok
            with open(file_path, "wb") as f:
                f.write(file.read())
            upf = await self.__send_data_to_db(data, file_path, complex_path, db)
        except ConnectionError as e:
            raise e
        return upf, ok
    

    async def __send_data_to_db(self, data, file_path, complex_path, db: AsyncSession):
        async with db as session:
            async with session.begin():
                data_to_db = data # filename, desc
                data_to_db["filepath"] = file_path
                data_to_db["size"] = os.path.getsize(file_path)//1024
                data_to_db["desc"] = data["desc"]
                data_to_db["upload_date"] = datetime.now().date()
                data_to_db["picture_path"] = f"{complex_path}/{data["picture_path"]}"
                data_to_db["proj_name"] = data["proj_name"]
                file_dal = TdimDals(session)
                up_file = await file_dal.upload_file(data_to_db)
                return up_file


    async def __file_existing_check(self, filename: str, name: str) ->  dict | bool :
        errs, execute_code = [], True
        if filename in os.listdir(f"{UPLOAD_DIRECTORY}/{name}"):
            errs.append({"existing error": "file is exist"})
            execute_code = False
        return errs, execute_code
    

    async def get_tdim_model(self, model_id, db: AsyncSession):
        async with db as session:
            tdim_dals = TdimDals(session)
            res = await tdim_dals.get_data_for_viewer(model_id=model_id)
            return res

    
    async def edit_model(self):
        ...
    

    async def reload_model(self):
        ...


    async def remove_model(self, tdim_id, db: AsyncSession):
        async with db as session:
            tdim_dals = TdimDals(session)
            data = await tdim_dals.get_path_from_id(tdim_id)
            try:
                os.remove(data["filepath"])
                os.remove(data["picpath"])
                os.removedirs(f"{UPLOAD_DIRECTORY}/{data["filename"]}")
            except KeyError as e:
                ...
            
            del_res = await tdim_dals.delete_tdim(tdim_id)
            return {"data": data, "count-del": del_res}