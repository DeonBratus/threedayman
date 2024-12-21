import os
import asyncio
from app.config import UPLOAD_DIRECTORY
from app.services.tdim_service import TDModelService

async def test():
    ffiles = await TDModelService().get_files_data()
    for f in ffiles.values():  # Исправлено: перебор значений из словаря
        print(f)
    return ffiles  # Возвращает словарь файлов

# Запуск асинхронной функции
if __name__ == "__main__":
    files = asyncio.run(test())  # Используем asyncio.run()
    print(files)  # Печатаем результат
