from DB.sql_session import sql_session
import DB.classes as classes
from decouple import config


remote_session = config('REMOTE_SESSION', cast=bool)


@sql_session(remote=remote_session)
def create(session, entry):
    session.add(entry)
    session.commit()


@sql_session(remote=remote_session)
def read(session, Class, id_: int = None):
    return session.query(Class).all() if id_ is None else session.get(Class, id_)


@sql_session(remote=remote_session)
def delete(session, entity):
    session.delete(entity)
    session.commit()


@sql_session(remote=remote_session)
def soft_delete(session, entity):
    if hasattr(entity, 'active'):
        entity.active = False
        session.commit()


@sql_session(remote=remote_session)
def get_user_by_username(session, username):
    return session.query(classes.User).filter(
        classes.User.username == username.strip()).first()
