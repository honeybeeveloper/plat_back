from sqlalchemy.sql.schema import (
    Column,
    ForeignKey,
    PrimaryKeyConstraint,
    ForeignKeyConstraint,
    Sequence
)
from sqlalchemy.sql.sqltypes import (
    DateTime,
    Integer,
    String,
)
from sqlalchemy.sql.functions import func

from ozz_backend.database.entity.base import Base


class UserQuestLogTB(Base):
    __tablename__ = 'user_quest_log_tb'

    id = Column(Integer, Sequence('user_quest_log_tb_id_seq'), primary_key=True)
    PrimaryKeyConstraint(name='user_quest_log_tb_pk')
    user_id = Column(Integer,
                     ForeignKey('user_proto_tb.id',
                                name='user_quest_log_tb_user_id',
                                onupdate='CASCADE',
                                ondelete='CASCADE')
                     )
    mission_id = Column(Integer)
    quest_id = Column(Integer)
    status = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, onupdate=func.now())

    ForeignKeyConstraint(columns=['mission_id', 'quest_id'],
                         refcolumns=['quest_bridge_tb.mission_id', 'quest_bridge_tb.quest_id'],
                         name='user_quest_log_tb_mission_quest_id',
                         ondelete='CASCADE', onupdate='CASCADE')

