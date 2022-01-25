import sqlalchemy
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sshtunnel import SSHTunnelForwarder
from decouple import config
from DB.sql_session import get_engine_for_port


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id_ = Column('id', sqlalchemy.Integer, primary_key=True)
    username = Column(
        sqlalchemy.String(length=30))
    password = Column(
        sqlalchemy.String(length=64))
    active = Column(sqlalchemy.Boolean, default=True)


class Article(Base):
    __tablename__ = 'articles'

    id_ = Column('id', sqlalchemy.Integer, primary_key=True)
    name = Column(
        sqlalchemy.String(length=30))
    description = Column(sqlalchemy.String(length=60))
    current_price = Column(sqlalchemy.Numeric)
    availability = Column(sqlalchemy.Integer)
    active = Column(sqlalchemy.Boolean, default=True)

    quotes = relationship('QuoteArticle', back_populates='article')


class Client(Base):
    __tablename__ = 'clients'

    id_ = Column('id', sqlalchemy.Integer, primary_key=True)
    identification_document = Column(
        sqlalchemy.String(length=30), unique=True)
    first_name = Column(
        sqlalchemy.String(length=30))
    last_name = Column(
        sqlalchemy.String(length=30))
    cellphone = Column(
        sqlalchemy.String(length=30))
    email = Column(
        sqlalchemy.String(length=30))
    address = Column(
        sqlalchemy.String(length=60))
    active = Column(sqlalchemy.Boolean, default=True)

    quotes = relationship('Quote', back_populates='client')


class Quote(Base):
    __tablename__ = 'quotes'

    id_ = Column('id', sqlalchemy.Integer, primary_key=True)
    client_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('clients.id'))
    generated_date = Column(sqlalchemy.Date)
    due_date = Column(sqlalchemy.Date)
    closed_date = Column(sqlalchemy.Date)
    total_cost = Column(sqlalchemy.Numeric)

    client = relationship('Client', back_populates='quotes')
    articles = relationship('QuoteArticle', back_populates='quote')
    invoices = relationship('Invoice', back_populates='quote')


class QuoteArticle(Base):
    __tablename__ = 'quote_article'

    quote_id = Column(sqlalchemy.Integer,
                      ForeignKey('quotes.id'), primary_key=True)
    article_id = Column(sqlalchemy.Integer,
                        ForeignKey('articles.id'), primary_key=True)
    quantity = Column(sqlalchemy.Integer)

    article = relationship('Article', back_populates='quotes')
    quote = relationship('Quote', back_populates='articles')


class Invoice(Base):
    __tablename__ = 'invoices'

    id_ = Column('id', sqlalchemy.Integer, primary_key=True)
    quote_id = Column(sqlalchemy.Integer,
                      ForeignKey('quotes.id'))
    payment = Column(sqlalchemy.Numeric)
    balance = Column(sqlalchemy.Numeric)

    quote = relationship('Quote', back_populates='invoices')


def main(remote=True):
    if remote:
        with SSHTunnelForwarder(
                (config('DB_SSH_IP'), config('DB_SSH_PORT', cast=int)),
                ssh_username=config('DB_SSH_USERNAME'),
                ssh_pkey=config('DB_SSH_KEY_PATH'),
                remote_bind_address=(config('DB_HOST'), config('DB_PORT', cast=int))
        ) as tunnel:
            tunnel.start()
            engine = get_engine_for_port(tunnel.local_bind_port)
            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)
    else:
        engine = get_engine_for_port(config('DB_PORT', cast=int))
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()
