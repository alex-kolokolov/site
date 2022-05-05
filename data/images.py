import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

roles_to_users = sqlalchemy.Table(
    'images_to_items',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('product_id', sqlalchemy.Integer(), sqlalchemy.ForeignKey('items.id')),
    sqlalchemy.Column('image_id', sqlalchemy.Integer(), sqlalchemy.ForeignKey('images.id'))
)


class Images(SqlAlchemyBase):
    __tablename__ = 'images'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    image = sqlalchemy.Column(sqlalchemy.String)
