from sqlalchemy.sql.schema import (
    Column,
    ForeignKey,
    PrimaryKeyConstraint,
    Sequence,
)
from sqlalchemy.sql.sqltypes import (
    DateTime,
    Integer,
)
from sqlalchemy.sql.functions import func

from ozz_backend.database.entity.base import Base


class MaterialBridgeTb(Base):
    __tablename__ = 'material_bridge_tb'

    id = Column(Integer, Sequence('material_bridge_tb'), primary_key=True)
    PrimaryKeyConstraint(name='material_bridge_tb_pk')
    mission_id = Column(Integer,
                        ForeignKey('mission_tb.id',
                                   name='material_bridge_tb_mission_id_fk',
                                   onupdate='CASCADE',
                                   ondelete='CASCADE'))

    # material_id = Column(Integer)
    material_id = Column(Integer,
                         ForeignKey('material_tb.id',
                                    name='material_bridge_tb_material_id_fk',
                                    onupdate='CASCADE',
                                    ondelete='CASCADE'))
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, onupdate=func.now())
