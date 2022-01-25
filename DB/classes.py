import sqlalchemy
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sql_session import remote_sql_session

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id_ = Column('id', sqlalchemy.Integer, primary_key=True)
    user_name = Column(
        sqlalchemy.String(length=30))
    password = Column(
        sqlalchemy.String(length=64))


class Article(Base):
    __tablename__ = 'articles'

    id_ = Column('id', sqlalchemy.Integer, primary_key=True)
    name = Column(
        sqlalchemy.String(length=30))
    description = Column(sqlalchemy.String(length=60))
    current_price = Column(sqlalchemy.Numeric)
    availability = Column(sqlalchemy.Integer)

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

    quotes = relationship('Quote', back_populates='client')


class Quote(Base):
    __tablename__ = 'quotes'

    id_ = Column('id', sqlalchemy.Integer, primary_key=True)
    client_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('clients.id'))
    generated_date = Column(sqlalchemy.Date)
    due_date = Column(sqlalchemy.Date)
    closed_date = Column(sqlalchemy.Date)
    total_cost = Column(sqlalchemy.Numeric)

    client = relationship('Client', back_populates='quote')
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


@remote_sql_session
def main(session, engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()
