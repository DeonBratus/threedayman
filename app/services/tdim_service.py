import os
from typing import BinaryIO
from config import UPLOAD_DIRECTORY
from datetime import datetime
from dals.tdim_dals import TdimDals
from sqlalchemy.ext.asyncio import AsyncSession
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
            upf = await self.__upload_file_info(data, file_path, complex_path, db)
        except ConnectionError as e:
            raise e
        return upf, ok
    

    async def __upload_file_info(self, data, file_path, complex_path, db: AsyncSession):
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


    async def upload_preview_picture(self, picture: BinaryIO, folder_name: str, picname: str):
        complex_path = f"{UPLOAD_DIRECTORY}/{folder_name}"
        file_path = os.path.join(complex_path, f"{picname}")

        with open(file_path, "wb") as pf:
            pf.write(picture.read())


    async def get_all_datafiles(self):
        file_names = os.listdir(UPLOAD_DIRECTORY)
        files = dict()
        for i in range(len(file_names)):
            size = os.path.getsize(f"{UPLOAD_DIRECTORY}/{file_names[i]}")//1024
            index_format = file_names[i].index('.')
            files[i] = {
                "filename": file_names[i], 
                "size": size, 
                "format": f"{file_names[i][index_format+1:]}"
            }
        return files


    async def file_existing_check(self, filename: str, name: str) ->  dict | bool :
        errs, execute_code = [], True
        if filename in os.listdir(f"{UPLOAD_DIRECTORY}/{name}"):
            errs.append({"existing error": "file is exist"})
            execute_code = False
        return errs, execute_code