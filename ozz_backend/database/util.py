from sqlalchemy.engine.row import Row
from ozz_backend.database.entity.base import Base


def to_dict(tuple, serialise=True, exclude_meta=True):
    """
    Convert a SQLAlchemy object to a dictionary
    :param serialise: Convert datetime to string if true (make JSON serializable)
    :param exclude_meta: Exclude metadata columns if true
    :return: dictionary
    """
    if isinstance(tuple, Base):
        return tuple.to_dict(serialise, exclude_meta)
    elif isinstance(tuple, Row):
        col_dic = {}
        for key, value in tuple._mapping.items():
            if isinstance(value, Base) or isinstance(value, Row):
                col_dic[key] = to_dict(value, serialise, exclude_meta)
            else:
                col_dic[key] = value
        return col_dic
    raise RuntimeError(f'Dictionary converter not available for type {type(tuple)}')
