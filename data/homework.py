import sqlalchemy

from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Homework(SqlAlchemyBase):
    __tablename__ = 'homework'

    group_chat_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('groups.group_chat_id'),
                                      primary_key=True)
    deadline = sqlalchemy.Column(sqlalchemy.Date)
    directory_path = sqlalchemy.Column(sqlalchemy.String)

    groups = orm.relation('Groups', back_populates='homework')
