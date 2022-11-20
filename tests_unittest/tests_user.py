from unittest.mock import ANY

from models import Session, Base, engine, UserSchema, User
from main import app

from werkzeug.security import generate_password_hash
from flask_testing import TestCase



class MyTest(TestCase):

	def setUp(self):
		app.config['SECURITY_KEY'] = '1'
		super().setUp()
		self.user_1_data = {
			"is_admin": True,
			"firstname": "a",
			"username": "user1",
			"lastname": "b",
			"email": "user1@gmail.com",
			"password": "11111111",
			"phone": "0671487080"
		}

		self.user_2_data = {
			"is_admin": False,
			"firstname": "aa",
			"username": "user2",
			"lastname": "bb",
			"email": "user2@gmail.com",
			"password": "22222222",
			"phone": "0671487080"
		}

		self.user_1_data_hashed = {
			"id": ANY,
			"is_admin": True,
			"firstname": "a",
			"username": "user1",
			"lastname": "b",
			"email": "user1@gmail.com",
			"password": ANY,
			"phone": "0671487080"
		}

		self.user_2_data_hashed = {
			"id": ANY,
			"is_admin": False,
			"firstname": "aa",
			"username": "user2",
			"lastname": "bb",
			"email": "user2@gmail.com",
			"password": ANY,
			"phone": "0671487080"
		}
		self.user_1_data_upd = {
			"is_admin": True,
			"firstname": "au",
			"username": "user11",
			"lastname": "bu",
			"email": "user1@gmail.com",
			"password": "11111111",
			"phone": "0671487080"
		}
		self.user_1_data_upd_hashed = {
			"id": ANY,
			"is_admin": True,
			"firstname": "au",
			"lastname": "bu",
			"email": "user1@gmail.com",
			"phone": "0671487080"
		}
		self.session = Session()

	def create_app(self):
		return app

	def close_session(self):
		self.session.close()

	def tearDown(self):
		self.close_session()


class NewUser(MyTest):
	def test1_new_admin(self):
		resp = self.client.post(
			"/user",
			json=self.user_1_data
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, self.user_1_data_hashed)

	def test2_new_user(self):
		resp = self.client.post(
			"/user",
			json=self.user_2_data
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, self.user_2_data_hashed)

	def test3_find_user_all(self):
		resp = self.client.get(
			"/user/findAll",
			auth=(self.user_1_data['username'], self.user_1_data['password'])
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, [self.user_1_data_hashed, self.user_2_data_hashed])

	def test4_find_user_by_username(self):
		resp = self.client.get(
			"/user/findUserByUsername?{}={}".format("username", "user1"),
			auth=(self.user_1_data['username'], self.user_1_data['password'])
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, self.user_1_data_hashed)

	def test5_update_user(self):
		user = self.session.query(User).filter(User.username == self.user_1_data['username']).first()
		resp = self.client.put(
			"/user/?{}={}".format("user_id", user.id),
			auth=(self.user_1_data['username'], self.user_1_data['password']),
			json=self.user_1_data_upd
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, self.user_1_data_upd_hashed)

	# def test6_find_user_bu_id(self):
	# 	resp = self.client.get(
	# 		"/user/findUserByUsername?{}={}".format("username", "user1"),
	# 		auth=(self.user_1_data['username'], self.user_1_data['password'])
	# 	)
	#
	# 	self.assertEqual(resp.status_code, 200)
	# 	self.assertEqual(resp.json, self.user_1_data_hashed)
