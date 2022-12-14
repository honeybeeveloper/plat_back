from sqlalchemy.sql.schema import (
    Column,
    ForeignKey,
    PrimaryKeyConstraint,
    Sequence,
)
from sqlalchemy.sql.sqltypes import (
    DateTime,
    Integer,
    String,
)
from sqlalchemy.sql.functions import func

from ozz_backend.database.entity.base import Base


class QuestBridgeTb(Base):
    __tablename__ = 'quest_bridge_tb'

    id = Column(Integer, Sequence('quest_bridge_tb'), primary_key=True)
    PrimaryKeyConstraint(name='quest_bridge_tb_pk')
    mission_id = Column(Integer,
                        ForeignKey('mission_tb.id',
                                   name='quest_bridge_tb_mission_id_fk',
                                   onupdate='CASCADE',
                                   ondelete='CASCADE'))
    quest_cd = Column(String)
    quest_id = Column(Integer,
                      ForeignKey('quest_tb.id',
                                 name='quest_bridge_tb_quest_id_fk',
                                 onupdate='CASCADE',
                                 ondelete='CASCADE'))
    quest_order = Column(Integer)
    link_quest_id = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, onupdate=func.now())
