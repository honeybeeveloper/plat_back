from sqlalchemy.sql.schema import (
    Column,
    ForeignKey,
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


class UserMissionLogTB(Base):
    __tablename__ = 'user_mission_log_tb'

    id = Column(Integer, Sequence('user_mission_log_tb_id_seq'), primary_key=True)
    PrimaryKeyConstraint(name='user_mission_log_tb_pk')
    user_id = Column(Integer,
                     ForeignKey('user_proto_tb.id',
                                name='user_mission_log_tb_user_id',
                                onupdate='CASCADE',
                                ondelete='CASCADE')
                     )
    mission_id = Column(Integer,
                        ForeignKey('mission_tb.id',
                                   name='user_mission_log_tb_mission_id',
                                   onupdate='CASCADE',
                                   ondelete='CASCADE')
                        )
    status = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, onupdate=func.now())
