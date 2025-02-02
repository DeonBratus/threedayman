from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
import uvicorn
from routers.tdim_router import tdim_router
from routers.project_router import proj_api

main_router = APIRouter()
main_router.include_router(tdim_router)
main_router.include_router(proj_api)

app = FastAPI()
app.include_router(main_router)
app.include_router
app.mount("/static", StaticFiles(directory="front"), name="static")
app.mount("/uploaded_files", StaticFiles(directory="uploaded_files"), name="uploaded_files")

if __name__ == "__main__":
    uvicorn.run(app="app:app", host="127.0.0.1", port=8000, reload=True )