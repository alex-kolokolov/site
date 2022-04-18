import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Furniture(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
  #  color = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("colors.id"))
  #  image = sqlalchemy.Column(sqlalchemy.String)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)