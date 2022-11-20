from unittest.mock import ANY

from models import Session, Base, engine, UserSchema
from main import app

from werkzeug.security import generate_password_hash
from flask_testing import TestCase



class MyTest(TestCase):

	def setUp(self):
		app.config['SECURITY_KEY'] = '1'
		super().setUp()
		self.create_tables()
		self.user_1_data = {
			"is_admin": 1,
			"firstname": "a",
			"username": "user1",
			"lastname": "b",
			"email": "user1@gmail.com",
			"password": "11111111",
			"phone": "0671487080"
		}

		self.user_2_data = {
			"is_admin": 1,
			"firstname": "aa",
			"username": "user2",
			"lastname": "bb",
			"email": "user2@gmail.com",
			"password": "22222222",
			"phone": "0671487080"
		}

		self.user_1_data_hashed = {
			"is_admin": True,
			"firstname": "a",
			"username": "user1",
			"lastname": "b",
			"email": "user1@gmail.com",
			"password": generate_password_hash(self.user_1_data['password']),
			"phone": "0671487080"
		}

		self.user_2_data_hashed = {
			"is_admin": True,
			"firstname": "aa",
			"username": "user2",
			"lastname": "bb",
			"email": "user2@gmail.com",
			"password": generate_password_hash(self.user_2_data['password']),
			"phone": "0671487080"
		}
		self.create_tables()
		self.session = Session()

	def create_tables(self):
		Base.metadata.drop_all(bind=engine)
		Base.metadata.create_all(bind=engine)

	def create_app(self):
		return app

	def close_session(self):
		self.session.close()

	def tearDown(self):
		self.close_session()


class NewUser(MyTest):
	# def test_new_user(self):
	# 	resp = self.client.post(
	# 		"/user",
	# 		json=self.user_1_data
	# 	)
	#
	# 	self.assertEqual(resp.status_code, 200)
	# 	self.assertEqual(resp.json, {
	# 		"id": ANY,
	# 		"is_admin": self.user_1_data_hashed['is_admin'],
	# 		"firstname": self.user_1_data_hashed['firstname'],
	# 		"username": self.user_1_data_hashed['username'],
	# 		"lastname": self.user_1_data_hashed['lastname'],
	# 		"email": self.user_1_data_hashed['email'],
	# 		"password": ANY,
	# 		"phone": self.user_1_data_hashed['phone']
	# 	})

	def test_find_user_all(self):
		user_schema = UserSchema()
		user = user_schema.load(self.user_2_data, session=self.session)
		user.password = generate_password_hash(user.password)
		self.session.add(user)
		self.session.commit()


		resp = self.client.get(
			"/user/findAll",
			auth=(self.user_2_data['username'], self.user_2_data['password'])
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, [{
			"id": ANY,
			"is_admin": self.user_2_data['is_admin'],
			"firstname": self.user_2_data['firstname'],
			"username": self.user_2_data['username'],
			"lastname": self.user_2_data['lastname'],
			"email": self.user_2_data['email'],
			"password": ANY,
			"phone": self.user_2_data['phone']
		}])

	def test_find_user_by_username(self):
		user_schema = UserSchema()
		user = user_schema.load(self.user_1_data, session=self.session)
		user.password = generate_password_hash(user.password)
		self.session.add(user)
		self.session.commit()


		resp = self.client.get(
			"/user/findUserByUsername?{}={}".format("username", "user1"),
			auth=(self.user_1_data['username'], self.user_1_data['password'])
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, {
			"id": ANY,
			"is_admin": self.user_1_data_hashed['is_admin'],
			"firstname": self.user_1_data_hashed['firstname'],
			"username": self.user_1_data_hashed['username'],
			"lastname": self.user_1_data_hashed['lastname'],
			"email": self.user_1_data_hashed['email'],
			"password": ANY,
			"phone": self.user_1_data_hashed['phone']
		})
