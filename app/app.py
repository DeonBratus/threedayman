from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
import uvicorn
from routers.tdim_router import tdim_router

main_router = APIRouter()
main_router.include_router(tdim_router)

app = FastAPI()
app.include_router(main_router)
app.mount("/static", StaticFiles(directory="front"), name="static")

if __name__ == "__main__":
    uvicorn.run(app="app:app", host="0.0.0.0", port=8000, reload=True )