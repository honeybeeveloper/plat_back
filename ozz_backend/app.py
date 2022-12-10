import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from ozz_backend import app_config
from ozz_backend.api import persona

# FastAPI app
app = FastAPI()

# TODO : CORS 등록
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# add api router
app.include_router(persona.router)


if __name__ == '__main__':
    uvicorn.run("app:app", host='127.0.0.1', port=8080, reload=app_config.app_reload)
