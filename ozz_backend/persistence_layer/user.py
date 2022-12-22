from datetime import datetime

from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from ozz_backend import app_logger
from ozz_backend.common.exception import ValueNotFoundEx, FailToUpdate
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

    @staticmethod
    def modify_user_ongoing_info(data):
        try:
            now = datetime.now()
            DBSession.query(entity.UserOngoingProtoTB)\
                .filter(entity.UserOngoingProtoTB.user_id == data.user_id)\
                .filter(entity.UserOngoingProtoTB.mission_id == data.mission_id) \
                .update({'quest_id': data.quest_id, 'modified_at': now})

            DBSession.commit()
        except SQLAlchemyError as e:
            app_logger.error(e)
            raise FailToUpdate('fail to update user_ongoing_proto_tb')
