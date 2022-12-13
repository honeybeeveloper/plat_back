from fastapi import APIRouter
from pydantic import BaseModel
from starlette.requests import Request

from ozz_backend import app_logger
from ozz_backend.persistence_layer import Mission


router = APIRouter(
    prefix="/mission",
    tags=["mission"],
    # dependencies=[Depends(get_token_header)],
)


class MissionInfoIn(BaseModel):
    mission_type: str


class MissionInfoOut(BaseModel):
    id: int
    title: str
    description: str
    material_id: int | None = None
    knowhow_id: int | None = None
    quest_id: int | None = None


@router.get('/test')
def test_api():
    app_logger.info('test')
    return {'test'}


@router.get('/{mission_type}', response_model=MissionInfoOut)
def get_mission(request: Request, mission_type: str):
    app_logger.info(f'[{request.method}] {request.url}: {request.client.host}:{request.client.port}')
    result = Mission.get_mission_info(mission_type)
    return MissionInfoOut(id=result.id, title=result.title, description=result.description,
                          material_id=result.material_id, knowhow_id=result.knowhow_id,
                          quest_id=result.quest_id).dict()
