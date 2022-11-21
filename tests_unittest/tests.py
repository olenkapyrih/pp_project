from unittest.mock import ANY

from models import *
from main import app

#from werkzeug.security import generate_password_hash
from flask_testing import TestCase



class UserCase(TestCase):

	def setUp(self):
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

		self.user_1_data_r = {
			"id": ANY,
			"is_admin": True,
			"firstname": "a",
			"username": "user1",
			"lastname": "b",
			"email": "user1@gmail.com",
			"password": ANY,
			"phone": "0671487080"
		}

		self.user_2_data_r = {
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
			"firstname": "au",
			"lastname": "bu",
		}
		self.user_1_data_upd_r = {
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


class UserTests(UserCase):
	def test1_new_admin(self):
		resp = self.client.post(
			"/user",
			json=self.user_1_data
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, self.user_1_data_r)

	def test1_new_admin_e(self):
		resp = self.client.post(
			"/user",
			json=self.user_1_data
		)

		self.assertEqual(resp.status_code, 400)

	def test2_new_user(self):
		resp = self.client.post(
			"/user",
			json=self.user_2_data
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, self.user_2_data_r)

	def test3_find_user_all(self):
		resp = self.client.get(
			"/user/findAll",
			auth=(self.user_1_data['username'], self.user_1_data['password'])
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, [self.user_1_data_r, self.user_2_data_r])

	def test3_find_user_all_e1(self):
		resp = self.client.get(
			"/user/findAll",
			auth=(self.user_2_data['username'], self.user_2_data['password'])
		)

		self.assertEqual(resp.status_code, 403)

	def test3_find_user_all_e2(self):
		resp = self.client.get(
			"/user/findAll"
		)

		self.assertEqual(resp.status_code, 401)

	def test4_find_user_by_username(self):
		resp = self.client.get(
			"/user/findUserByUsername?{}={}".format("username", self.user_1_data['username']),
			auth=(self.user_1_data['username'], self.user_1_data['password'])
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, self.user_1_data_r)

	def test4_find_user_by_username_e(self):
		resp = self.client.get(
			"/user/findUserByUsername?{}={}".format("username", ""),
			auth=(self.user_1_data['username'], self.user_1_data['password'])
		)

		self.assertEqual(resp.status_code, 404)

	def test5_find_user_by_id(self):
		user = self.session.query(User).filter(User.username == self.user_1_data['username']).first()
		resp = self.client.get(
			"/user/findUserByID/?{}={}".format("user_id", user.id),
			auth=(self.user_1_data['username'], self.user_1_data['password'])
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, self.user_1_data_r)

	def test6_update_user(self):
		user = self.session.query(User).filter(User.username == self.user_1_data['username']).first()
		resp = self.client.put(
			"/user/?{}={}".format("user_id", user.id),
			auth=(self.user_1_data['username'], self.user_1_data['password']),
			json=self.user_1_data_upd
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, self.user_1_data_upd_r)

	def test6_update_user_e1(self):
		resp = self.client.put(
			"/user/?{}={}".format("user_id", 555555),
			auth=(self.user_1_data['username'], self.user_1_data['password']),
			json=self.user_1_data_upd
		)

		self.assertEqual(resp.status_code, 404)

	def test6_update_user_e2(self):
		user = self.session.query(User).filter(User.username == self.user_1_data['username']).first()
		resp = self.client.put(
			"/user/?{}={}".format("user_id", user.id)
		)

		self.assertEqual(resp.status_code, 401)

	def test6_update_user_e3(self):
		user = self.session.query(User).filter(User.username == self.user_2_data['username']).first()
		resp = self.client.put(
			"/user/?{}={}".format("user_id", user.id),
			auth=(self.user_1_data['username'], self.user_1_data['password']),
			json=self.user_1_data_upd
		)

		self.assertEqual(resp.status_code, 403)

	def test7_delete_user1(self):
		resp = self.client.delete(
			"/user/?{}={}".format("user_id", 9999999),
			auth=(self.user_1_data['username'], self.user_1_data['password'])
		)
		self.assertEqual(resp.status_code, 404)

	def test7_delete_user1(self):
		user = self.session.query(User).filter(User.username == self.user_2_data['username']).first()
		resp = self.client.delete(
			"/user/?{}={}".format("user_id", user.id)
		)
		self.assertEqual(resp.status_code, 401)

	def test7_delete_user3(self):
		user = self.session.query(User).filter(User.username == self.user_2_data['username']).first()
		resp = self.client.delete(
			"/user/?{}={}".format("user_id", user.id),
			auth=(self.user_1_data['username'], self.user_1_data['password'])
		)
		self.assertEqual(resp.status_code, 200)

		user = self.session.query(User).filter(User.username == self.user_1_data['username']).first()
		resp = self.client.delete(
			"/user/?{}={}".format("user_id", user.id),
			auth=(self.user_1_data['username'], self.user_1_data['password'])
		)
		self.assertEqual(resp.status_code, 200)



class TourCase(TestCase):

	def setUp(self):
		super().setUp()
		self.session = Session()

		self.tour_data_1 = {
		    "name": "tourName",
		    "price": 1000,
		    "photoUrl": "https://stackoverflow.com",
		    "is_available": True
		}
		self.tour_data_1_r = {
			"id": ANY,
			"name": "tourName",
			"price": 1000,
			"photoUrl": "https://stackoverflow.com",
			"is_available": True
		}
		self.tour_data_2 = {
		    "name": "tourName2",
		    "price": 2000,
		    "photoUrl": "https://stackoverflow.ua",
		    "is_available": False
		}
		self.tour_data_2_r = {
			"id": ANY,
			"name": "tourName2",
			"price": 2000,
			"photoUrl": "https://stackoverflow.ua",
			"is_available": False
		}
		self.tour_data_1_upd = {
			"name": "tourName",
			"price": 10001,
			"photoUrl": "https://stackoverflow.comu",
			"is_available": True
		}
		self.tour_data_1_upd_r = {
			"id": ANY,
			"name": "tourName",
			"price": 10001,
			"photoUrl": "https://stackoverflow.comu",
			"is_available": True
		}
		self.admin_data = {
			"is_admin": True,
			"firstname": "a",
			"username": "user1",
			"lastname": "b",
			"email": "user1@gmail.com",
			"password": "11111111",
			"phone": "0671487080"
		}

	def create_app(self):
		return app

	def close_session(self):
		self.session.close()

	def tearDown(self):
		self.close_session()


class TourTests(TourCase):

	def test1_new_tour_iat(self):
		resp = self.client.post(
			"/user",
			json=self.admin_data
		)
		resp = self.client.post(
			"/tour",
			json=self.tour_data_1,
			auth=(self.admin_data['username'], self.admin_data['password'])
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, self.tour_data_1_r)


	def test2_new_tour_iaf(self):
		resp = self.client.post(
			"/tour",
			json=self.tour_data_2,
			auth=(self.admin_data['username'], self.admin_data['password'])
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, self.tour_data_2_r)

	def test2_new_tour_iaf_e1(self):
		resp = self.client.post(
			"/tour",
			json=self.tour_data_2
		)

		self.assertEqual(resp.status_code, 401)

	def test2_new_tour_iaf_e2(self):
		resp = self.client.post(
			"/tour",
			json=self.admin_data,
			auth=(self.admin_data['username'], self.admin_data['password'])
		)

		self.assertEqual(resp.status_code, 400)

	def test3_find_tour_all(self):
		resp = self.client.get(
			"/tour/findAll"
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, [self.tour_data_1_r, self.tour_data_2_r])

	def test4_find_tour_by_status(self):
		resp = self.client.get(
			"/tour/findByStatus?{}={}".format("tour_status", 1),
			auth=(self.admin_data['username'], self.admin_data['password'])
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, [self.tour_data_1_r])

	def test4_find_tour_by_status_e(self):
		resp = self.client.get(
			"/tour/findByStatus?{}={}".format("tour_status", 4),
			auth=(self.admin_data['username'], self.admin_data['password'])
		)

		self.assertEqual(resp.status_code, 400)

	def test5_find_tour_by_id(self):
		tour = self.session.query(Tour).filter(Tour.name == self.tour_data_1['name']).first()
		resp = self.client.get(
			"/tour/findByID/?{}={}".format("tour_id", tour.id),
			auth=(self.admin_data['username'], self.admin_data['password'])
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, self.tour_data_1_r)

	def test5_find_tour_by_id_e1(self):
		tour = self.session.query(Tour).filter(Tour.name == self.tour_data_1['name']).first()
		resp = self.client.get(
			"/tour/findByID/?{}={}".format("tour_id", tour.id)
		)

		self.assertEqual(resp.status_code, 401)

	def test5_find_tour_by_id_e2(self):
		tour = self.session.query(Tour).filter(Tour.name == self.tour_data_1['name']).first()
		resp = self.client.get(
			"/tour/findByID/?{}={}".format("tour_id", 999999),
			auth=(self.admin_data['username'], self.admin_data['password'])
		)

		self.assertEqual(resp.status_code, 404)

	def test6_update_user(self):
		tour = self.session.query(Tour).filter(Tour.name == self.tour_data_1['name']).first()
		resp = self.client.put(
			"/tour?{}={}".format("tour_id", tour.id),
			auth=(self.admin_data['username'], self.admin_data['password']),
			json=self.tour_data_1_upd
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, self.tour_data_1_upd_r)

	def test7_delete_tour(self):
		tour = self.session.query(Tour).filter(Tour.name == self.tour_data_1['name']).first()
		resp = self.client.delete(
			"/tour/?{}={}".format("tour_id", tour.id),
			auth=(self.admin_data['username'], self.admin_data['password'])
		)
		self.assertEqual(resp.status_code, 200)

		tour = self.session.query(Tour).filter(Tour.name == self.tour_data_2['name']).first()
		resp = self.client.delete(
			"/tour/?{}={}".format("tour_id", tour.id),
			auth=(self.admin_data['username'], self.admin_data['password'])
		)
		self.assertEqual(resp.status_code, 200)

		user = self.session.query(User).filter(User.username == self.admin_data['username']).first()
		resp = self.client.delete(
			"/user/?{}={}".format("user_id", user.id),
			auth=(self.admin_data['username'], self.admin_data['password'])
		)


class OrderCase(TestCase):

	def setUp(self):
		super().setUp()
		self.session = Session()

		self.tour_data = {
		    "name": "tourName",
		    "price": 1000,
		    "photoUrl": "https://stackoverflow.com",
		    "is_available": True
		}
		self.admin_data = {
			"is_admin": True,
			"firstname": "a",
			"username": "user1",
			"lastname": "b",
			"email": "user1@gmail.com",
			"password": "11111111",
			"phone": "0671487080"
		}
		self.order_data = {
			"quantity": 1,
			"ordering_date": "2022-10-15",
			"status": "approved"
		}
		self.order_data_r = {
			"id": ANY,
			"user_id": ANY,
			"tour_id": ANY,
			"quantity": 1,
			"ordering_date": "2022-10-15",
			"status": "approved"
		}
		self.order_data_upd = {
			"quantity": 2,
			"ordering_date": "2222-12-22",
			"status": "approved"
		}
		self.order_data_upd_r = {
			"id": ANY,
			"user_id": ANY,
			"tour_id": ANY,
			"quantity": 2,
			"ordering_date": "2222-12-22",
			"status": "approved"
		}

	def create_app(self):
		return app

	def close_session(self):
		self.session.close()

	def tearDown(self):
		self.close_session()


class OrderTests(OrderCase):
	def test0_preparation(self):
		resp = self.client.post(
			"/user",
			json=self.admin_data
		)
		resp = self.client.post(
			"/tour",
			json=self.tour_data,
			auth=(self.admin_data['username'], self.admin_data['password'])
		)

	def test1_new_order(self):
		user = self.session.query(User).filter(User.username == self.admin_data['username']).first()
		tour = self.session.query(Tour).filter(Tour.name == self.tour_data['name']).first()

		self.order_data['user_id'] = user.id
		self.order_data['tour_id'] = tour.id

		resp = self.client.post(
			"/order",
			json=self.order_data,
			auth=(self.admin_data['username'], self.admin_data['password'])
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, self.order_data_r)

	def test2_find_order_all(self):
		resp = self.client.get(
			"/order/findAll",
			auth=(self.admin_data['username'], self.admin_data['password'])
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, [self.order_data_r])

	def test3_find_order_by_id(self):
		order = self.session.query(Order).first()
		resp = self.client.get(
			"/order/findByID/?{}={}".format("order_id", order.id),
			auth=(self.admin_data['username'], self.admin_data['password'])
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, self.order_data_r)

	def test4_find_order_by_user_id(self):
		user = self.session.query(User).first()
		resp = self.client.get(
			"/order/findByUserID?{}={}".format("user_id", user.id),
			auth=(self.admin_data['username'], self.admin_data['password'])
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, [self.order_data_r])

	def test5_update_order(self):
		order = self.session.query(Order).first()

		self.order_data_upd['user_id'] = order.user_id
		self.order_data_upd['tour_id'] = order.tour_id
		resp = self.client.put(
			"/order?{}={}".format("order_id", order.id),
			auth=(self.admin_data['username'], self.admin_data['password']),
			json=self.order_data_upd
		)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, self.order_data_upd_r)

	def test6_delete_order(self):
		order = self.session.query(Order).first()
		resp = self.client.delete(
			"/order/?{}={}".format("order_id", order.id),
			auth=(self.admin_data['username'], self.admin_data['password'])
		)

		tour = self.session.query(Tour).first()
		resp = self.client.delete(
			"/tour/?{}={}".format("tour_id", tour.id),
			auth=(self.admin_data['username'], self.admin_data['password'])
		)

		user = self.session.query(User).first()
		resp = self.client.delete(
			"/user/?{}={}".format("user_id", user.id),
			auth=(self.admin_data['username'], self.admin_data['password'])
		)
