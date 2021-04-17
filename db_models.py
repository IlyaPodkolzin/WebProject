from sqlalchemy import orm, Column, Integer, String, DateTime, ForeignKey, Table
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime
from db_session import ORMBase

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
    checks = orm.relation('Check', secondary='expenses', back_populates='users')

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
    __tablename__ = 'check'
    id = Column(Integer, primary_key=True, autoincrement=True)
    str_Qr = Column(String, nullable=False)
    id_type = Column(Integer, ForeignKey('type.id'))
    users = orm.relation('User', secondary='expenses', back_populates='check')
    time_added = Column(DateTime, nullable=False, default=datetime.datetime.now)
    information = Column(String, nullable=False, default='Просто чек')

    def __init__(self, str_Qr, id_type, time, info):
        self.str_Qr = str_Qr
        self.id_type = id_type
        self.information = info
        self.time_added = time


class Expenses(ORMBase):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('users.id'))
    id_check = Column(Integer, ForeignKey('check.id'))
    all_expenses = Column(nullable=False, default={1: 0, 2: 0,
                                                   3: 0, 4: 0,
                                                   5: 0, 6: 0,
                                                   7: 0, 8: 0,
                                                   9: 0, 10: 0,
                                                   11: 0, 12: 0})
    type_expens = Column(nullable=False, default={1: {}, 2: {},
                                                  3: {}, 4: {},
                                                  5: {}, 6: {},
                                                  7: {}, 8: {},
                                                  9: {}, 10: {},
                                                  11: {}, 12: {}})

    def __init__(self, user, check, expense, type_):
        self.id_user = user
        self.id_check = check
        self.all_expenses[int(datetime.datetime.now().month)] += expense
        self.type_expens[int(datetime.datetime.now().month)][type_] += expense
