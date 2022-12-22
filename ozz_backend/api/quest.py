from fastapi import APIRouter
from pydantic import BaseModel
from starlette.requests import Request

from ozz_backend import app_logger
from ozz_backend.persistence_layer import Quest, User


router = APIRouter(
    prefix="/quest",
    tags=["quest"],
    # dependencies=[Depends(get_token_header)],
)


class MessageOut(BaseModel):
    message: str


class QuestOut(BaseModel):
    id: int
    quest_name: str | None = None
    description: str | None = None
    thumbnail_path: str | None = None
    quest_cd: str
    quest_order: int
    link_quest_id: int | None = None
    link_quest_cd: str | None = None


class QuestOutList(BaseModel):
    quests: list[dict]


class UserQuest(BaseModel):
    user_id: int
    mission_id: int
    quest_id: int
    quest_order: int
    status: str | None
    is_last: bool | None


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


@router.get('/mission-quest-order')
def get_quest(request: Request, mission_id: int, quest_order: int):
    app_logger.info(f'[{request.method}] {request.url}: {request.client.host}:{request.client.port}')
    result = Quest.get_quest_with_mission_id_quest_order(mission_id=mission_id, quest_order=quest_order)
    return QuestOut(id=result.quest_id,
                    quest_cd=result.quest_cd,
                    quest_order=result.quest_order)


@router.post('/completion', response_model=UserQuest)
def add_user_quest_log(request: Request, ongoing_data: UserQuest):
    app_logger.info(f'[{request.method}] {request.url}: {request.client.host}:{request.client.port}')
    # 1. update user_quest_log_tb
    Quest.modify_user_quest_log(ongoing_data)

    if not ongoing_data.is_last:
        next_quest_order = ongoing_data.quest_order + 1
        # 2. get next quest id
        result = Quest.get_quest_with_mission_id_quest_order(mission_id=ongoing_data.mission_id,
                                                             quest_order=next_quest_order)
        ongoing_data.quest_id = result.quest_id
        # 3. update user_ongoig_proto_tb
        User.modify_user_ongoing_info(ongoing_data)
        # 4. insert user_quest_log_tb (new data, status = 'O')
        ongoing_data.status = 'O'
        Quest.add_user_quest_log(ongoing_data)

    return UserQuest(user_id=ongoing_data.user_id, mission_id=ongoing_data.mission_id,
                     quest_id=ongoing_data.quest_id, quest_order=ongoing_data.quest_order,
                     status=None, is_last=None)
