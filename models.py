from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
	__tablename__ = "user"

	id = Column('id', Integer, primary_key=True)
	is_admin = Column('is_admin', Boolean)
	firstname = Column('firstname', String(45))
	lastname = Column('lastname', String(45))
	email = Column('email', String(128))
	password = Column('password', String(45))
	phone = Column('phone', String(12))


class Ordering(Base):
	__tablename__ = "ordering"

	id = Column('id', Integer, primary_key=True)
	quantity = Column('quantity', Integer)
	ordering_date = Column('ordering_date', Date)
	status = Column('status', String(45))
	tour_id = Column('tour_id', ForeignKey('tour.id'))
	user_id = Column('user_id', ForeignKey('user.id'))


class Tour(Base):
	__tablename__ = "tour"

	id = Column('id', Integer, primary_key=True)
	name = Column('name', String(45))
	price = Column('price', Integer)
	photoUrl = Column('photoUrl', String(2048))
	available = Column('available', Boolean)



source = open("connect_string.txt", "r")
engine = create_engine(source.readline())
Base.metadata.create_all(bind=engine)