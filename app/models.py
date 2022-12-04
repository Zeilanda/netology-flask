import uuid
from typing import Type

import config
from cachetools import cached
from sqlalchemy import Column, Integer, String, DateTime, create_engine, func, Table, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import EmailType, UUIDType


Base = declarative_base()


association_table = Table(
    "association_table",
    Base.metadata,
    Column("owners_id", ForeignKey("owners.id")),
    Column("adverts_id", ForeignKey("adverts.id"))
)


class Owner(Base):
    __tablename__ = "owners"
    id = Column(Integer, primary_key=True)
    email = Column(EmailType, unique=True)
    password = Column(String(32), nullable=False)
    advert = relationship("Advert", secondary=association_table)


class Advert(Base):
    __tablename__ = "adverts"
    id = Column(Integer, primary_key=True)
    ad_header = Column(String(30), nullable=False)
    description = Column(String(200), nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Token(Base):

    __tablename__ = "tokens"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("owners.id", ondelete="CASCADE"))
    user = relationship("Owner", lazy="joined")


@cached({})
def get_engine():
    return create_engine(config.PG_DSN)


@cached({})
def get_session_maker():
    return sessionmaker(binf=get_engine())


def init_db():
    Base.metadata.create_all(bind=get_engine())


def close_db():
    get_engine().dispose()


ORM_MODEL_CLS = Type[Owner] | Type[Token] | Type[Advert]
ORM_MODEL = Owner | Token | Advert