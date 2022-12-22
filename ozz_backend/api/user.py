from fastapi import APIRouter
from pydantic import BaseModel
from starlette.requests import Request

from ozz_backend import app_logger
from ozz_backend.persistence_layer import User


router = APIRouter(
    prefix="/user",
    tags=["user"],
    # dependencies=[Depends(get_token_header)],
)


class UserOngoingOut(BaseModel):
    user_id: str
    mission_id: int
    quest_id: int


@router.get('/test')
def test_api():
    app_logger.info('test')
    return {'test'}


@router.get('/user-ongoing', response_model=UserOngoingOut)
def get_ongoing_info(request: Request, user_id: int, mission_id: int):
    app_logger.info(f'[{request.method}] {request.url}: {request.client.host}:{request.client.port}')
    result = User.get_user_ongoing_info(user_id, mission_id)
    ongoing = UserOngoingOut(user_id=result.user_id, mission_id=result.mission_id, quest_id=result.quest_id)
    return ongoing
