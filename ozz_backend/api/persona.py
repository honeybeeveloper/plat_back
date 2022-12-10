from fastapi import APIRouter
from pydantic import BaseModel
from starlette.requests import Request

from ozz_backend import app_logger
from ozz_backend.persistence_layer.mission import Mission


router = APIRouter(
    prefix="/persona",
    tags=["persona"],
    # dependencies=[Depends(get_token_header)],
)


class MissionInfoIn(BaseModel):
    mission_type: str


class MissionInfoOut(BaseModel):
    title: str
    description: str
    material_id: int | None = None
    knowhow_id: int | None = None
    quest_id: int | None = None


@router.get('/test')
def test_api():
    app_logger.info('test')
    return {'test'}


@router.get('/mission', response_model=MissionInfoOut)
def get_mission(request: Request):
    app_logger.info(f'[{request.method}] {request.url}: {request.client.host}:{request.client.port}')
    result = Mission.get_mission_info('mission_persona_analysis')
    return MissionInfoOut(title=result.title, description=result.description,
                          material_id=result.material_id, knowhow_id=result.knowhow_id,
                          quest_id=result.quest_id).dict()
