import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

roles_to_users = sqlalchemy.Table(
    'materials_to_items',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('products_id', sqlalchemy.Integer(), sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('material_id', sqlalchemy.Integer(), sqlalchemy.ForeignKey('roles.id'))
)


class Material(SqlAlchemyBase):
    __tablename__ = 'materials'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    material = sqlalchemy.Column(sqlalchemy.String)
    image = orm.relation("Image")