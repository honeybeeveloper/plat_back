from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from ozz_backend import app_logger
from ozz_backend.common.exception import ValueNotFoundEx, FailToInsertion, FailToUpdate
from ozz_backend.database import entity
from ozz_backend.database.conn import DBSession


class Mission(object):
    @staticmethod
    def get_mission_info(mission_type):
        try:
            mission_info = DBSession.query(entity.MissionTB)\
                .filter(entity.MissionTB.mission_type == mission_type)\
                .one()
            return mission_info
        except NoResultFound as e:
            app_logger.error(e)
            raise ValueNotFoundEx('mission info not found')

    @staticmethod
    def add_ongoing_mission(user_id, mission_id):
        try:
            DBSession.add(entity.UserOngoingProtoTB(user_id=user_id,
                                                    mission_id=mission_id,
                                                    quest_id=1))
            DBSession.commit()
        except SQLAlchemyError as e:
            app_logger.error(e)
            raise FailToInsertion('fail to insert into user_ongoing_proto_tb')

    @staticmethod
    def add_user_mission_log(data):
        try:
            DBSession.add(entity.UserMissionLogTB(user_id=data.user_id,
                                                  mission_id=data.mission_id,
                                                  status=data.status))
            DBSession.commit()
        except SQLAlchemyError as e:
            app_logger.error(e)
            raise FailToInsertion('fail to insert into user_mission_log_tb')

    @staticmethod
    def update_user_mission_log(data):
        try:
            DBSession.query(entity.UserMissionLogTB)\
                .filter(entity.UserMissionLogTB.user_id == data.user_id)\
                .filter(entity.UserMissionLogTB.mission_id == data.mission_id)\
                .update({'status': data.status})

            DBSession.commit()
        except SQLAlchemyError as e:
            app_logger.error(e)
            raise FailToUpdate('fail to update user_mission_log_tb')
