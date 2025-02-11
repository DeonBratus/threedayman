from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Монтируем статические файлы (если нужно отдавать файлы напрямую)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Путь к локальной папке, которую вы хотите отобразить
LOCAL_FOLDER = "../../uploaded_files"

@app.get("/api/files")
def get_files(path: str = ""):
    """
    Возвращает список файлов и папок в указанной директории.
    """
    target_path = os.path.join(LOCAL_FOLDER, path)
    if not os.path.exists(target_path):
        return {"error": "Directory not found"}

    items = []
    for item in os.listdir(target_path):
        item_path = os.path.join(target_path, item)
        items.append({
            "name": item,
            "type": "directory" if os.path.isdir(item_path) else "file",
            "path": os.path.join(path, item)
        })
    return {"path": path, "items": items}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)