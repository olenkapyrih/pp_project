from uuid import UUID

from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, scoped_session
from sqlalchemy_serializer import SerializerMixin
from marshmallow_sqlalchemy import *

engine = create_engine("mysql+pymysql://root:2004@localhost:3306/ppdb")
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
Base = declarative_base()
Base.metadata.create_all(bind=engine)


class CustomSerializerMixin(SerializerMixin):
	serialize_types = (
		(UUID, lambda x: str(x)),
	)


class User(Base, CustomSerializerMixin):
	__tablename__ = "user"

	serialize_only = {'id', 'is_admin', 'firstname', 'lastname', 'email', 'password', 'phone'}

	id = Column('id', Integer, primary_key=True, autoincrement=True)
	is_admin = Column('is_admin', Boolean, nullable=False)
	firstname = Column('firstname', String(45), nullable=False)
	username = Column('username', String(20), nullable=False)
	lastname = Column('lastname', String(45), nullable=False)
	email = Column('email', String(128), nullable=False)
	password = Column('password', String(45), nullable=False)
	phone = Column('phone', String(12), nullable=False)


class Order(Base, CustomSerializerMixin):
	__tablename__ = "order"

	serialize_only = {'id', 'quantity', 'ordering_date', 'status', 'tour_id', 'user_id'}

	id = Column('id', Integer, primary_key=True)
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


# class TourSchema(SQLAlchemyAutoSchema):
# 	model = Tour
# 	include_relationships = True
# 	load_instance = True


Base.metadata.create_all(bind=engine)

