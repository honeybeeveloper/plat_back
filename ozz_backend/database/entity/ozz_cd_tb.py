from sqlalchemy.sql.schema import (
    Column,
    PrimaryKeyConstraint,
)
from sqlalchemy.sql.sqltypes import (
    DateTime,
    String,
)
from sqlalchemy.sql.functions import func

from ozz_backend.database.entity.base import Base


class OzzCdTb(Base):
    __tablename__ = 'ozz_cd_tb'
    __table_args__ = (
        PrimaryKeyConstraint('cd_id', 'cd_type', name='ozz_cd_tb_pk'),
    )

    cd_id = Column(String)
    cd_type = Column(String)
    cd_name = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, onupdate=func.now())
