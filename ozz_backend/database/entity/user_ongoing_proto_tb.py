from sqlalchemy.sql.schema import (
    Column,
    PrimaryKeyConstraint,
    Sequence,
    ForeignKey
)
from sqlalchemy.sql.sqltypes import (
    DateTime,
    Integer,
    String,
)
from sqlalchemy.sql.functions import func

from ozz_backend.database.entity.base import Base


class UserOngoingProtoTB(Base):
    __tablename__ = 'user_ongoing_proto_tb'

    id = Column(Integer, Sequence('user_proto_tb_id_seq'), primary_key=True)
    PrimaryKeyConstraint(name='user_ongoing_proto_tb_pk')
    user_id = Column(Integer,
                     ForeignKey('user_proto_tb.id',
                                name='user_ongoing_proto_tb_user_id',
                                onupdate='CASCADE',
                                ondelete='CASCADE'))
    mission_id = Column(Integer,
                        ForeignKey('mission_tb.id',
                                   name='user_ongoing_proto_tb_mission_id',
                                   onupdate='CASCADE',
                                   ondelete='CASCADE'))
    quest_id = Column(Integer,
                      ForeignKey('quest_tb.id',
                                 name='user_ongoing_proto_tb_quest_id',
                                 onupdate='CASCADE',
                                 ondelete='CASCADE'))
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, onupdate=func.now())
