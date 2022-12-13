from sqlalchemy.exc import NoResultFound

from ozz_backend import app_logger
from ozz_backend.common.exception import ValueNotFoundEx
from ozz_backend.database import entity
from ozz_backend.database.conn import DBSession


class Material(object):
    @staticmethod
    def get_material_with_mission_id(mission_id):
        return DBSession.query(entity.MaterialTB.id,
                               entity.MaterialTB.material_name,
                               entity.MaterialTB.material_type,
                               entity.MaterialTB.thumbnail_path,
                               entity.OzzCdTb.cd_name)\
                .join(entity.MaterialBridgeTb, entity.MaterialTB.id == entity.MaterialBridgeTb.material_id)\
                .join(entity.OzzCdTb, entity.MaterialTB.material_type == entity.OzzCdTb.cd_id)\
                .filter(entity.MaterialBridgeTb.mission_id == mission_id)\
                .all()
