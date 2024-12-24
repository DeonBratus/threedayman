import os
import asyncio
from app.config import UPLOAD_DIRECTORY
from app.services.tdim_service import TdimService

async def test():
    ffiles = await TdimService().get_all_datafiles()
    for f in ffiles.values():  # Исправлено: перебор значений из словаря
        print(f)
    return ffiles  # Возвращает словарь файлов

# Запуск асинхронной функции
if __name__ == "__main__":
    files = asyncio.run(test())  # Используем asyncio.run()
    print(files)  # Печатаем результат
