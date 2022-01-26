from DB.sql_session import remote_sql_session


@remote_sql_session
def create(session, entry):
    session.add(entry)
    session.commit()


@remote_sql_session
def read(session, Class, id_: int = None):
    return session.query(Class).all() if id_ is None else session.get(Class, id_)


@remote_sql_session
def delete(session, entity):
    session.delete(entity)
    session.commit()


@remote_sql_session
def soft_delete(session, entity):
    if hasattr(entity, 'active'):
        entity.active = False
        session.commit()
