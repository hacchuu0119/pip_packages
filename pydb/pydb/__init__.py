from .connection import Connection

CONNECTION_MYSQL = None


def setup_connection_instance_mysql():
    global CONNECTION_MYSQL
    CONNECTION_MYSQL = Connection()


def _get_connection_instance_mysql():
    if not CONNECTION_MYSQL:
        setup_connection_instance_mysql()

    return CONNECTION_MYSQL


def mysql(user=None, password=None,
          host=None, port=None, database=None, *args, **kwargs):
    return _get_connection_instance_mysql().create_connection_mysql(user=user,
                                                                    password=password,
                                                                    host=host,
                                                                    port=port,
                                                                    database=database,
                                                                    *args, **kwargs)


CONNECTION_ORACLE = None


def setup_connection_instance_oracle():
    global CONNECTION_ORACLE
    CONNECTION_ORACLE = Connection()


def _get_connection_instance_oracle():
    if not CONNECTION_ORACLE:
        setup_connection_instance_oracle()

    return CONNECTION_ORACLE


def oracle(user=None, password=None,
           host=None, port=None, sid=None, *args, **kwargs):
    return _get_connection_instance_oracle().create_connection_oracle(user=user,
                                                                      password=password,
                                                                      host=host,
                                                                      port=port,
                                                                      sid=sid,
                                                                      *args, **kwargs)
