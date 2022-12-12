from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import (
    Column,
    PrimaryKeyConstraint,
    Sequence
)
from sqlalchemy.sql.sqltypes import (
    DateTime,
    Integer,
    String,
)
from sqlalchemy.sql.functions import func

from ozz_backend.database.entity.base import Base


class MissionTB(Base):
    __tablename__ = 'mission_tb'

    id = Column(Integer, Sequence('mission_tb_id_seq'), primary_key=True)
    PrimaryKeyConstraint(name='mission_tb_pk')
    mission_type = Column(String)
    title = Column(String)
    description = Column(String)
    material_id = Column(Integer)
    knowhow_id = Column(Integer)
    quest_id = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, onupdate=func.now())

    # material_bridge_tb_relation = relationship('MaterialBridgeTb',
    #                                            back_populates='mission_tb',
    #                                            cascade='all, delete')
