from sqlalchemy import orm, Column, Integer, String, DateTime, ForeignKey, Table
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime
from data.db_session import ORMBase

type_table = Table('type', ORMBase.metadata,
                   Column('id', Integer, primary_key=True, autoincrement=True),
                   Column('name', String, nullable=False))


class User(ORMBase, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    inn = Column(Integer, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    inn_password = Column(String, nullable=False)

    def __init__(self, name, email, password, inn):
        self.name = name
        self.email = email
        self.inn_password = password
        self.inn = inn

    def set_password(self, password):
        self.inn_password = password

    def check_password(self, password):
        return check_password_hash(generate_password_hash(self.inn_password), password)


class Check(ORMBase):
    __tablename__ = 'checks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    str_Qr = Column(String, nullable=False)
    id_type = Column(Integer, ForeignKey('type.id'))
    time_added = Column(DateTime, nullable=False, default=datetime.datetime.now)
    information = Column(String, nullable=False, default='Просто чек')
    id_user = Column(Integer, ForeignKey('users.id'))

    def __init__(self, str_Qr, id_type, info, user):
        self.id_user = user
        self.str_Qr = str_Qr
        self.id_type = id_type
        self.information = info
