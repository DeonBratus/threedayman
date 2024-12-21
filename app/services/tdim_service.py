import os
from typing import BinaryIO
from config import UPLOAD_DIRECTORY
#Services of td-project
#This service for only manage 3D
class TDModelService:

    async def upload_file(self, file: BinaryIO, data: dict) -> dict | bool:
        file_path = os.path.join(UPLOAD_DIRECTORY, data["raw_filename"])
        msg, ok = await self.__full_check_file(filename=data["raw_filename"])

        # Check uploaded file
        if not ok: 
            return msg, ok
        
        # Save file to folder
        with open(file_path, "wb") as f:
            f.write(file.read())
        return {"file size": data["raw_filename"]}, ok
    

    async def __upload_file_info(self, data):
        ...
        


    async def get_files_data(self):
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


    async def __full_check_file(self, filename) ->  dict | bool :
        errs, execute_code = [], True
        if filename in os.listdir(UPLOAD_DIRECTORY):
            errs.append({"existing error": "file is exist"})
            execute_code = False
        # if ".stl" not in filename.lower():
        #     errs.append({"format error": "file is not stl"})
        #     execute_code = False
        return errs, execute_code