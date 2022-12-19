from sqlalchemy.exc import NoResultFound

from ozz_backend import app_logger
from ozz_backend.common.exception import ValueNotFoundEx
from ozz_backend.database import entity
from ozz_backend.database.conn import DBSession


class User(object):
    @staticmethod
    def get_user_ongoing_info(user_id, mission_id):
        try:
            user_ongoing_info = DBSession.query(entity.UserProtoTB.user_id,
                                                entity.UserOngoingProtoTB.mission_id,
                                                entity.UserOngoingProtoTB.quest_id)\
                .filter(entity.UserProtoTB.id == entity.UserOngoingProtoTB.user_id)\
                .filter(entity.UserProtoTB.id == user_id) \
                .filter(entity.UserOngoingProtoTB.mission_id == mission_id) \
                .one()
            return user_ongoing_info
        except NoResultFound as e:
            app_logger.error(e)
            raise ValueNotFoundEx('user ongoing info not found')
