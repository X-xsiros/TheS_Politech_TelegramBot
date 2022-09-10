import sqlalchemy

from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Groups(SqlAlchemyBase):
    __tablename__ = 'groups'

    group_chat_id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    members = sqlalchemy.Column(sqlalchemy.String, default='')

    homework = orm.relationship('Homework', back_populates='groups')
    literature = orm.relationship('Literature', back_populates='groups')
    materials = orm.relationship('Materials', back_populates='groups')
