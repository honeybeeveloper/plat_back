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


@router.get('/test')
def test_api():
    app_logger.info('test')
    return {'test'}


@router.get('/mission-quests', response_model=QuestOutList)
def get_materials(request: Request, mission_id: int):
    app_logger.info(f'[{request.method}] {request.url}: {request.client.host}:{request.client.port}')
    results = Quest.get_quest_with_mission_id(mission_id)
    quests = [QuestOut(id=result.id,
                       quest_name=result.quest_name,
                       description=result.description,
                       thumbnail_path=result.thumbnail_path,
                       quest_cd=result.quest_cd,
                       quest_order=result.quest_order,
                       link_quest_id=result.link_quest_id,
                       link_quest_cd=result.link_quest_cd).dict() for result in results]
    return {'quests': quests}
