from datetime import datetime

from sqlalchemy.inspection import inspect
from sqlalchemy.ext.declarative import declarative_base


class Base(object):
    def to_dict(self, serialise=True, exclude_meta=True):
        """
        Convert an entity object to dictionary
        :param serialise: Convert datetime to string if true (make JSON serializable)
        :param exclude_meta: Exclude metadata columns if true
        :return: dictionary
        """
        col_dic = {}
        for col_attr in inspect(self).mapper.column_attrs:
            if exclude_meta and col_attr.key in ('created_at', 'created_by', 'modified_at', 'modified_by'):
                continue
            col_val = getattr(self, col_attr.key)
            if serialise and isinstance(col_val, datetime):
                col_val = col_val.strftime('%Y-%m-%d %H:%M:%S.%f')
            col_dic[col_attr.key] = col_val
        return col_dic


Base = declarative_base(cls=Base)
