from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def db_connect():

    return create_engine("sqlite:///authors.db", echo=False)


def create_table(engine):
    Base.metadata.create_all(engine)


class Authors(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    url = Column(String(250), nullable=False)

    quotes = relationship('Quotes', back_populates='authors')


class Quotes(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    quote = Column(String(250), nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=True)

    authors = relationship('Authors', back_populates='quotes')
    tag_in_quote = relationship('TagInQuote', back_populates='quotes')


class Tags(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(String(250), nullable=False)

    tag_in_quote = relationship('TagInQuote', back_populates='tags')


class TagInQuote(Base):
    __tablename__ = "tag_in_quote"
    id = Column(Integer, primary_key=True, autoincrement=True)
    quotes_id = Column(Integer, ForeignKey('quotes.id'), nullable=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=True)

    quotes = relationship('Quotes', back_populates='tag_in_quote')
    tags = relationship('Tags', back_populates='tag_in_quote')


class AboutAuthor(Base):
    __tablename__ = "about_author"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    birthday = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)