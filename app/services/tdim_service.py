import os
from typing import BinaryIO
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from config import UPLOAD_DIRECTORY
from dals.tdim_dals import TdimDals
'''
Services of 3d-project. This service for only manage files
There is logic of managment files only.
'''

class TdimService:

    async def upload_file(self, file: BinaryIO, data: dict, db: AsyncSession) -> dict | bool:
        complex_path = f"{UPLOAD_DIRECTORY}/{data["filename"]}"
        os.makedirs(complex_path, exist_ok=True)
        try:
            file_path = os.path.join(complex_path, data["raw_filename"])
            msg, ok = await self.file_existing_check(filename=data["raw_filename"], name=data["filename"])
            # Check uploaded file
            if not ok: 
                return msg, ok
            # Save file to folder
            with open(file_path, "wb") as f:
                f.write(file.read())
            # Send data to db
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
                data_to_db["upload_date"] = datetime.now().date()
                data_to_db["picture_path"] = f"{complex_path}/{data["picture_path"]}"
                file_dal = TdimDals(session)
                up_file = await file_dal.upload_file(data_to_db)
                return up_file


    async def file_existing_check(self, filename: str, name: str) ->  dict | bool :
        errs, execute_code = [], True
        if filename in os.listdir(f"{UPLOAD_DIRECTORY}/{name}"):
            errs.append({"existing error": "file is exist"})
            execute_code = False
        return errs, execute_code
    
