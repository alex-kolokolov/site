import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Furniture(SqlAlchemyBase):
    __tablename__ = 'items'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    #  color = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("colors.id"))
    image = orm.relation("Images", secondary='images_to_items', backref='items')

    def __str__(self):
        return self.id
