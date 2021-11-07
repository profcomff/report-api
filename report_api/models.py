
import enum
from uuid import uuid4
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Enum
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


class ResponseOption(enum.Enum):
    yes = 1
    no = 2


class UnionMember(Model):
    __tablename__ = 'union_member'

    id = Column(Integer, primary_key=True)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    patronymic = Column(String)
    academic_group_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    email_uuid = Column(String, nullable=False, default=lambda:str(uuid4()))
    status = Column(Enum(Status), default=Status.unconfirmed)
    token = Column(String(256))
    password = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    answers = relationship('Answer', back_populates='union_member')


class Question(Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    index = Column(Integer, nullable=False)
    text = Column(String, nullable=False)

    answers = relationship('Answer', back_populates='question')


class Answer(Model):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    union_member_id = Column(Integer, ForeignKey(
        'union_member.id'), nullable=False)
    question_id = Column(Integer, ForeignKey(
        'questions.id'), nullable=False)
    answer = Column(Enum(ResponseOption), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    union_member = relationship('UnionMember', back_populates='answers')
    question = relationship('Question', back_populates='answers')
