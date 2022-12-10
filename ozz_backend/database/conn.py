from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker

from ozz_backend import app_config, app_logger


# TODO : learn this!
def create_db_engine():
    # https://docs.sqlalchemy.org/en/14/core/pooling.html
    return create_engine(url=f'postgresql+psycopg2://{app_config.database.user}:{app_config.database.password}@'
                             f'{app_config.database.host}:{app_config.database.port}/{app_config.database.database}',
                         echo=True,
                         # the size of the pool to be maintained, defaults to 5
                         pool_size=10,
                         # When the number of checked-out connections reaches the size set in pool_size,
                         # additional connections will be returned up to this limit.
                         # Defaults to 10
                         max_overflow=10,
                         # connection that has been open for more than one hour will be invalidated and replaced,
                         pool_recycle=3600)


# TODO : learn this!
def create_db_session(db_engine, scoped=True):
    if scoped:
        return scoped_session(sessionmaker(bind=db_engine))
    else:
        Session = sessionmaker(bind=db_engine)
        return Session()


engine = create_db_engine()
DBSession = create_db_session(engine)
