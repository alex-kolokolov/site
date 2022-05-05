import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

roles_to_users = sqlalchemy.Table(
    'roles_to_users',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user_id', sqlalchemy.Integer(), sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('role_id', sqlalchemy.Integer(), sqlalchemy.ForeignKey('roles.id'))
)


class Role(SqlAlchemyBase):
    __tablename__ = 'roles'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    def __str__(self):
        return self.name
