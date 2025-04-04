from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
import uvicorn
from models.tdim_dbmodel import init_db
from routers.tdim_router import tdim_router
from routers.project_router import proj_api
from routers.gallery_router import gallery_router

main_router = APIRouter()
main_router.include_router(tdim_router)
main_router.include_router(proj_api)
main_router.include_router(gallery_router)

app = FastAPI()
app.include_router(main_router)

app.mount("/static", StaticFiles(directory="front"), name="static")
app.mount("/uploaded_files", StaticFiles(directory="uploaded_files"), name="uploaded_files")

@app.on_event("startup")
async def on_startup():
    await init_db()

if __name__ == "__main__":
    uvicorn.run(app="app:app", host="0.0.0.0", port=8000, reload=True )