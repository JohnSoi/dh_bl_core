from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped

from utils import camel_to_snake_case

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    @classmethod
    def __tablename__(cls):
        return camel_to_snake_case(cls.__name__)

    id: Mapped[int] = Column(Integer, primary_key=True)
