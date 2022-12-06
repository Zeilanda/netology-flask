
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
DSN = "postgresql://app:1234@127.0.0.1:5431/netology"


class Advert(Base):

    __tablename__ = "adverts"

    id = Column(Integer, primary_key=True)
    ad_header = Column(String(30), nullable=False)
    description = Column(String(200), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    owner = Column(String(30), nullable=False)
