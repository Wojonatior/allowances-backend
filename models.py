import jwt
from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
from sqlalchemy.ext.declarative import declarative_base
from passlib.apps import custom_app_context as pwd_context

engine = create_engine('postgresql:///allowances_development', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hash = Column(String)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
    
    def generate_token(self):
        # FIXME: pull in an actual secret token here, instead of part of a jwt payload
        return jwt.encode({'user': self.username}, 'qwertyuiop1234567890', algorithm='HS256')

    def decode_token(token):
        return jwt.decode(token, 'qwertyuiop1234567890', algorithm='HS256')

    def validate_token(self, token):
        decode_token = decode_token(token)
        return decoded_token == {'user': self.username}

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hired_on = Column(DateTime, default=func.now())
    department_id = Column(Integer, ForeignKey('department.id'))
    department = relationship(
        Department,
        backref=backref('employees',
                        uselist=True,
                        cascade='delete,all'))
