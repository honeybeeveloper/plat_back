from fastapi import APIRouter
from pydantic import BaseModel
from starlette.requests import Request

from ozz_backend import app_logger
from ozz_backend.persistence_layer import Quest


router = APIRouter(
    prefix="/quest",
    tags=["quest"],
    # dependencies=[Depends(get_token_header)],
)


class MessageOut(BaseModel):
    message: str


class QuestIn(BaseModel):
    mission_id: str


class QuestOut(BaseModel):
    id: int
    quest_name: str
    description: str
    thumbnail_path: str
    quest_cd: str
    quest_order: int
    link_quest_id: int | None = None
    link_quest_cd: str | None = None


class QuestOutList(BaseModel):
    quests: list[dict]


class UserQuest(BaseModel):
    user_id: int
    mission_id: int
    status: str


@router.get('/test')
def test_api():
    app_logger.info('test')
    return {'test'}


@router.get('/mission-quests', response_model=QuestOutList)
def get_quests(request: Request, mission_id: int):
    app_logger.info(f'[{request.method}] {request.url}: {request.client.host}:{request.client.port}')
    results = Quest.get_quests_with_mission_id(mission_id)
    quests = [QuestOut(id=result.id,
                       quest_name=result.quest_name,
                       description=result.description,
                       thumbnail_path=result.thumbnail_path,
                       quest_cd=result.quest_cd,
                       quest_order=result.quest_order,
                       link_quest_id=result.link_quest_id,
                       link_quest_cd=result.link_quest_cd).dict() for result in results]
    return {'quests': quests}


# TODO : insert into user_quest_log_tb
# when user start mission, add related data in user_mission_log_tb
@router.post('/user-log', response_model=MessageOut)
def add_user_mission_log(request: Request, ongoing_data: UserQuest):
    app_logger.info(f'[{request.method}] {request.url}: {request.client.host}:{request.client.port}')
    # Quest.add_user_mission_log(user_id=ongoing_data.user_id,
    #                            mission_id=ongoing_data.mission_id,
    #                            status=ongoing_data.status)
    # return {'message': 'success to add'}
    pass


# TODO : update user_quest_log_tb
# when user finish the mission, update status
@router.patch('/user-log', response_model=MessageOut)
def update_user_mission_log(request: Request, ongoing_data: UserQuest):
    app_logger.info(f'[{request.method}] {request.url}: {request.client.host}:{request.client.port}')
    # Quest.update_user_mission_log(user_id=ongoing_data.user_id,
    #                               mission_id=ongoing_data.mission_id,
    #                               status=ongoing_data.status)
    # return {'message': 'success to update'}
    pass
