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
                               entity.OzzCdTB.cd_name)\
                .join(entity.MaterialBridgeTB, entity.MaterialTB.id == entity.MaterialBridgeTB.material_id)\
                .join(entity.OzzCdTB, entity.MaterialTB.material_type == entity.OzzCdTB.cd_id)\
                .filter(entity.MaterialBridgeTB.mission_id == mission_id)\
                .all()
