import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Colors(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    color = sqlalchemy.Column(sqlalchemy.String)