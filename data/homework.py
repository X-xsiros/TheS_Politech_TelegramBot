import sqlalchemy

from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Homework(SqlAlchemyBase):
    __tablename__ = 'homework'

    group_chat_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('groups.group_chat_id'))
    deadline = sqlalchemy.Column(sqlalchemy.Date)
    homework_id = sqlalchemy.Column(sqlalchemy.String,primary_key= True)
    some_text = sqlalchemy.Column(sqlalchemy.String)

    groups = orm.relation('Groups', back_populates='homework')

