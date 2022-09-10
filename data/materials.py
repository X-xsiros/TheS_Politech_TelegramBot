import sqlalchemy

from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Materials(SqlAlchemyBase):
    __tablename__ = 'materials'

    group_chat_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('groups.group_chat_id'),
                                      primary_key=True)
    lesson_date = sqlalchemy.Column(sqlalchemy.Date)
    directory_path = sqlalchemy.Column(sqlalchemy.String)

    groups = orm.relation('Groups', back_populates='materials')
