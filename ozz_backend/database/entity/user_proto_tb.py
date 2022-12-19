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


class UserProtoTB(Base):
    __tablename__ = 'user_proto_tb'

    id = Column(Integer, Sequence('user_proto_tb_id_seq'), primary_key=True)
    PrimaryKeyConstraint(name='user_proto_tb_pk')
    user_id = Column(String)
    user_password = Column(String)
    user_name = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, onupdate=func.now())
