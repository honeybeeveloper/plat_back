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


class MessageOut(BaseModel):
    message: str


class MissionInfoIn(BaseModel):
    mission_type: str


class MissionInfoOut(BaseModel):
    id: int
    title: str
    description: str
    material_id: int | None = None
    knowhow_id: int | None = None
    quest_id: int | None = None


class UserMission(BaseModel):
    user_id: int
    mission_id: int
    status: str


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


# TODO : insert into user_ongoing_proto_tb
# when user start mission, add related data in user_ongoing_proto_tb
@router.post('/ongoing-mission', response_model=MessageOut)
def add_ongoing_mission(request: Request, ongoing_data: UserMission):
    app_logger.info(f'[{request.method}] {request.url}: {request.client.host}:{request.client.port}')
    Mission.add_ongoing_mission(user_id=ongoing_data.user_id, mission_id=ongoing_data.mission_id)
    return {'message': 'success to add'}


# TODO : insert into user_mission_log_tb
# when user start mission, add related data in user_mission_log_tb
@router.post('/user-log', response_model=MessageOut)
def add_user_mission_log(request: Request, mission_data: UserMission):
    app_logger.info(f'[{request.method}] {request.url}: {request.client.host}:{request.client.port}')
    Mission.add_user_mission_log(user_id=mission_data.user_id,
                                 mission_id=mission_data.mission_id,
                                 status=mission_data.status)
    return {'message': 'success to add'}


# TODO : update user_mission_log_tb
# when user finish the quest, update status
@router.patch('/user-log', response_model=MessageOut)
def update_user_mission_log(request: Request, ongoing_data: UserMission):
    app_logger.info(f'[{request.method}] {request.url}: {request.client.host}:{request.client.port}')
    Mission.update_user_mission_log(user_id=ongoing_data.user_id,
                                    mission_id=ongoing_data.mission_id,
                                    status=ongoing_data.status)
    return {'message': 'success to update'}
