from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers.tdprinters_router import printers_api

main_router = APIRouter()
main_router.include_router(printers_api)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
        "http://127.0.0.1:8000", 
        "http://0.0.0.0:8000", 
        "http://192.168.31.66:8000",
        "https://dgd22g40-8000.euw.devtunnels.ms"]
        ,  # Укажите адрес основного приложения
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все HTTP-методы (GET, POST, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
    expose_headers=["*"]  # Важно для доступа к кастомным заголовкам
)

app.include_router(main_router)
app.mount("/static", StaticFiles(directory="front"), name="static")
app.mount("/uploaded_files", StaticFiles(directory="uploaded_files"), name="uploaded_files")

if __name__ == "__main__":
    uvicorn.run(app="app:app", host="0.0.0.0", port=8001, reload=True )