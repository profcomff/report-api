from uuid import uuid4

import enum
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey


@as_declarative()
class Model:
    pass


class Status(enum.Enum):
    unconfirmed = 1
    confirmed = 2
    finished = 3


class UnionMember(Model):
    __tablename__ = 'union_member'

    id = Column(Integer, primary_key=True)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    patronymic = Column(String)
    academic_group_number = Column(String, nullable=False)
    email = Column(String, primary_key=True, nullable=False)
    email_uuid = Column(String, nullable=False, default=str(uuid4()))
    status = Column(Enum(Status), default=Status.unconfirmed)
