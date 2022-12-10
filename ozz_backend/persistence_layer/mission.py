from sqlalchemy.exc import NoResultFound

from ozz_backend import app_logger
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
