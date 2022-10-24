from sqlalchemy.orm import sessionmaker
from order_status import Status
from models import *


source = open("connect_string.txt", "r")
engine = create_engine(source.readline())
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
user = User(
	id=1,
	is_admin=False,
	firstname='Ray',
	lastname='Smith',
	email='raymondo@gmail.com',
	password='qwerty123',
	phone='380683859139'
	)
ordering = Ordering(
	id=1,
	quantity=3,
	ordering_date='2022-01-19',
	status=Status.approved.name,
	tour_id=1,
	user_id=1
)
tour = Tour(
	id=1,
	name='Philippines',
	price=2000,
	photoUrl='https://i.natgeofe.com/n/04505c35-858b-4e95-a1a7-d72e5418b7fc/steep-karst-cliffs-of-el-nido-in-palawan.jpg?w=2880&h=1440',
	available=True
)

session.add(user)
session.commit()
session.add(tour)
session.commit()
session.add(ordering)
session.commit()

session.close()