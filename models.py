from uuid import UUID
# from flask import fields
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, scoped_session
from sqlalchemy.sql.functions import now
from sqlalchemy_serializer import SerializerMixin
from marshmallow_sqlalchemy import *
from marshmallow import fields, validate
from validators import *


source = open("E:\PythonProjects\pp_project\connect_string.txt", "r")
engine = create_engine(source.readline())
# engine = create_engine("mysql+pymysql://root:root1234@localhost:3306/tour")
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
Base = declarative_base()
Base.metadata.create_all(bind=engine)


class CustomSerializerMixin(SerializerMixin):
    serialize_types = (
        (UUID, lambda x: str(x)),
    )


def validate_phone(phone_number):
    temp = 0
    for i in phone_number:
        if i.isalpha():
            temp += 1
    if temp > 0 or len(phone_number) < 1 or len(phone_number) > 13:
        return False
    return True


def validate_entry_id(entry, entry_id):
    if Session.query(entry).filter(entry.id == entry_id).count() == 0:
        return False
    return True


def validate_tour_status(num):
    if num == "1" and num == "0":
        return True
    return False


def validate_order_status(status):
    if status not in ["approved", "received", "placed"]:
        return False
    return True
def validate_username(username1):

    if not (Session.query(User).filter(User.username==username1).count()==0):
        return False
    if len(username1) < 1 or len(username1)>20:
        return False
    return True
class User(Base, CustomSerializerMixin):
    __tablename__ = "user"

    # def __init__(self, id, is_admin, firstname, username, lastname, email, password, phone):
    # 	self.id = id
    # 	self.is_admin = is_admin
    # 	self.firstname = firstname
    # 	self.username = username
    # 	self.lastname = lastname
    # 	self.email = email
    # 	self.password = password
    # 	self.phone = phone

    serialize_only = {'id', 'is_admin', 'firstname', 'lastname', 'email', 'phone'}

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    is_admin = Column('is_admin', Boolean, nullable=False)
    firstname = Column('firstname', String(45), nullable=False)
    username = Column('username', String(20), nullable=False)
    lastname = Column('lastname', String(45), nullable=False)
    email = Column('email', String(128), nullable=False)
    password = Column('password', String(200), nullable=False)
    phone = Column('phone', String(12), nullable=False)


class Order(Base, CustomSerializerMixin):
    __tablename__ = "order"

    serialize_only = {'id', 'quantity', 'ordering_date', 'status', 'tour_id', 'user_id'}

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    quantity = Column('quantity', Integer, nullable=False)
    ordering_date = Column('ordering_date', Date, nullable=False)
    status = Column('status', String(45), nullable=False)
    tour_id = Column('tour_id', ForeignKey('tour.id'), nullable=False)
    user_id = Column('user_id', ForeignKey('user.id'), nullable=False)


class Tour(Base, CustomSerializerMixin):
    __tablename__ = "tour"

    serialize_only = {'id', 'name', 'price', 'photoUrl', 'is_available'}

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(45), nullable=False)
    price = Column('price', Integer, nullable=False)
    photoUrl = Column('photoUrl', String(2048), nullable=False)
    is_available = Column('is_available', Boolean, nullable=False)


class TourSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tour
        include_relationships = False
        load_instance = True
        include_fk = True

    #id = fields.Integer(validate=validate_entry_id)
    name = fields.String(validate=validate.Length(min=5, max=20))
    price = fields.Integer(validate=validate.Range(min=100, max=1000000))
    photoUrl = fields.String(validate=validate.URL())
    is_available = fields.Boolean(data_key="is_available")


class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Order
       # include_relationships = False
        load_instance = True
        #include_fk = True

    quantity = fields.Integer(validate=validate.Range(1, 100))
    ordering_date = fields.Date(format="iso")
    status = fields.String(validate=validate_order_status)
    tour_id = fields.Integer()
    user_id = fields.Integer()


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = False
        load_instance = True
        include_fk = True

    is_admin = fields.Boolean(data_key="is_admin")
    firstname = fields.String(validate=validate.Length(min=1, max=20))
    username = fields.String(validate=validate_username)
    lastname = fields.String(validate=validate.Length(min=1, max=25))
    email = fields.String(validate=validate.Email())
    password = fields.String(validate=validate.Length(min=8, max=25))
    phone = fields.String(validate=validate_phone)


Base.metadata.create_all(bind=engine)
