import sqlalchemy

from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Literature(SqlAlchemyBase):
    __tablename__ = 'literature'

    group_chat_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('groups.group_chat_id'),
                                      primary_key=True)
    directory_path = sqlalchemy.Column(sqlalchemy.String)

    groups = orm.relation('Groups', back_populates='literature')
