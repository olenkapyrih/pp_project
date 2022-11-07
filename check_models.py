from sqlalchemy.orm import sessionmaker
from order_status import Status
from models import *


engine = create_engine('mysql+pymysql://root:2004@localhost:3306/ppdb')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

users = [
	User(
		id=1,
		is_admin=False,
		firstname='Ray',
		lastname='Smith',
		username='raysmith',
		email='raymondo@gmail.com',
		password='qwerty123',
		phone='380683859139'),

	User(
		id=2, is_admin=True, firstname='Mickey', lastname='Pearson', username='mickeypearson', email='miki@gmail.com', password='qwerty', phone='380655859130')
]

orderings = [
	Order(
		id=1,
		quantity=3,
		ordering_date='2022-01-19',
		status=Status.approved.name,
		tour_id=1,
		user_id=1
	),
	Order(
	id=2,
	quantity=1,
	ordering_date='2020-02-14',
	status=Status.received.name,
	tour_id=2,
	user_id=1
	),
	Order(
		id=3,
		quantity=1,
		ordering_date='2020-02-14',
		status=Status.received.name,
		tour_id=2,
		user_id=2
	)
]
tours = [Tour(
	id=1,
	name='Philippines',
	price=2000,
	photoUrl='https://i.natgeofe.com/n/04505c35-858b-4e95-a1a7-d72e5418b7fc/steep-karst-cliffs-of-el-nido-in-palawan.jpg?w=2880&h=1440',
	is_available=1
	),
	Tour(
	id=2,
	name='Maldives',
	price=2600,
	photoUrl='https://i.natgeofe.com/n/04505c35-858b-4e95-a1a7-d72e5418b7fc/steep-karst-cliffs-of-el-nido-in-palawan.jpg?w=2880&h=1440',
	is_available=1
)
]

session.add_all(users)
session.commit()
session.add_all(tours)
session.commit()
session.add_all(orderings)
session.commit()

session.close()