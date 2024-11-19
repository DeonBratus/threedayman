import os
from typing import BinaryIO
from config import UPLOAD_DIRECTORY


class TDModelService:
    async def upload_file(self, file: BinaryIO, filename: str) -> dict | bool:
        file_path = os.path.join(UPLOAD_DIRECTORY, filename)
        msg, ok = await self.full_check_file(filename=filename)
        if not ok:
            return msg, ok
        with open(file_path, "wb") as f:
            f.write(file.read())
        return {"file size": filename}, ok
    

    async def read_upload_files(self):
        file_names = os.listdir(UPLOAD_DIRECTORY)
        files = dict()
        for f in file_names:
            files[f] = os.path.getsize(f"{UPLOAD_DIRECTORY}/{f}")
        return files


    async def full_check_file(self, filename) ->  dict | bool :
        errs, execute_code = [], True
        if filename in await self.read_upload_files():
            errs.append({"existing error": "file is exist"})
            execute_code = False
        if ".stl" not in filename.lower():
            errs.append({"format error": "file is not stl"})
            execute_code = False
        return errs, execute_code