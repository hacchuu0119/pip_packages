from sqlalchemy import create_engine
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base


class Connection:
    def __init__(self):
        self.session = None
        self.Base = None
        self.engine = None

    def create_connection_mysql(self, *args, user, password, host, port, database, **kwargs):

        jdbc_url = f'mysql://{user}:{password}@{host}:{port}/{database}?charset=utf8'

        return self._create_connection(jdbc_url, *args, **kwargs)

    def create_connection_oracle(self, *args, user, password, host, port, sid, **kwargs):
        jdbc_url = f'oracle://{user}:{password}@{host}:{port}/{sid}'
        return self._create_connection(jdbc_url, *args, **kwargs)

    def _create_connection(self, jdbc_url, *args, **kwargs):
        self.engine = create_engine(
            jdbc_url,
            connect_args=kwargs
        )
        return self.engine

    def create_session(self, autocommit=False, autoflush=False):
        # Sessionの作成(ORM)
        self.session = scoped_session(
            sessionmaker(
                autocommit=autocommit,
                autoflush=autoflush,
                bind=self.engine
            )
        )
        # modelで使用

    def model_base(self):
        self.Base = declarative_base()
        self.Base.query = self.session.query_property()
        return self.Base
