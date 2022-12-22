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


class QuestTB(Base):
    __tablename__ = 'quest_tb'

    id = Column(Integer, Sequence('quest_tb_id_seq'), primary_key=True)
    PrimaryKeyConstraint(name='quest_tb_pk')
    quest_name = Column(String)
    description = Column(String)
    thumbnail_path = Column(String)
    btn_1_type = Column(Integer)
    btn_2_type = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, onupdate=func.now())
