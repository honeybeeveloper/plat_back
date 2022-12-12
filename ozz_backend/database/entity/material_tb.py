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


class MaterialTB(Base):
    __tablename__ = 'material_tb'

    id = Column(Integer, Sequence('material_tb_id_seq'), primary_key=True)
    PrimaryKeyConstraint(name='material_tb_pk')
    material_name = Column(String)
    material_type = Column(String)
    thumbnail_path = Column(String)
    material_detail_id = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, onupdate=func.now())

    # material_bridge_tb_relation = relationship('MaterialBridgeTb',
    #                                            back_populates='material_tb',
    #                                            cascade='all, delete')
