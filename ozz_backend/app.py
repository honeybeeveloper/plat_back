import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from ozz_backend import app_config, app_logger
from ozz_backend.api import material, mission, quest, user
from ozz_backend.common.exception import OzzException

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
app.include_router(mission.router)
app.include_router(material.router)
app.include_router(quest.router)
app.include_router(user.router)


# add exception manager
@app.exception_handler(OzzException)
async def exception_handler(request: Request, ex: OzzException):
    app_logger.error(f'[{request.method}] {request.url}: {request.client.host}:{request.client.port}')
    return JSONResponse(status_code=ex.status_code, content=ex.detail)


if __name__ == '__main__':
    uvicorn.run("app:app", host='127.0.0.1', port=5000, reload=app_config.app_reload)
