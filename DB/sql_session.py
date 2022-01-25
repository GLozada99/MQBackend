from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import wraps
from decouple import config


def get_engine_for_port(port):
    return create_engine('postgresql+psycopg2://'
                         '{user}:{password}@{host}:{port}/{db}'.format(
                            user=config('DB_USER'),
                            password=config('DB_PASSWORD'),
                            host=config('DB_HOST'),
                            port=port,
                            db=config('DB_NAME')))


def with_sql_session(function, args, kwargs, engine=None):
    if engine is None:
        # Default to local port
        engine = get_engine_for_port(config('DB_PORT', cast=int))
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        return function(session, engine, *args, **kwargs)
    finally:
        session.close()


def with_local_sql_session(function, *args, **kwargs):
    return with_sql_session(function, args, kwargs)


def with_remote_sql_session(function, *args, **kwargs):
    # Hat tip: https://stackoverflow.com/a/38001815
    with SSHTunnelForwarder(
            (config('DB_SSH_IP'), config('DB_SSH_PORT', cast=int)),
            ssh_username=config('DB_SSH_USERNAME'),
            ssh_pkey=config('DB_SSH_KEY_PATH'),
            remote_bind_address=(config('DB_HOST'), config('DB_PORT', cast=int))
    ) as tunnel:
        tunnel.start()
        engine = get_engine_for_port(tunnel.local_bind_port)
        return with_sql_session(function, args, kwargs, engine=engine)


# Decorators
def local_sql_session(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return with_local_sql_session(function, *args, **kwargs)
    return wrapper


def remote_sql_session(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return with_remote_sql_session(function, *args, **kwargs)
    return wrapper
