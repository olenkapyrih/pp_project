from flask import request, Flask
from flask_sqlalchemy import SQLAlchemy
from models import *
import json

app = Flask(__name__)

from flask_marshmallow import *
from marshmallow import *
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2004@localhost:3306/ppdb'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


# ma = Marshmallow(app)
# db = SQLAlchemy(app)
'''queries dealing with tours table'''


@app.route('/tour', methods=['PUT'])
def update_tour():
    args = request.args
    tour_id = args.get("tour_id")
    args = request.get_json()
    session.query(Tour).filter(Tour.id == tour_id).update(args)
    session.commit()
    tour = session.query(Tour).filter(Tour.id == tour_id)[0].to_dict()
    return tour


@app.route('/tour', methods=['POST'])
def create_tour():
    args = request.get_json()
    new_tour = Tour(**args)
    session.add(new_tour)
    session.commit()
    return new_tour.to_dict()


@app.route('/tour/findAll', methods=['GET'])
def find_all_tours():
    tours = session.query(Tour)
    return json.dumps([i.to_dict() for i in tours])


@app.route('/tour/findByID', methods=['GET'])
def find_tour_by_id():
    args = request.args
    tour_id = args.get('tour_id')
    tours = session.query(Tour).filter(Tour.id == tour_id)
    return json.dumps([i.to_dict() for i in tours])


@app.route('/tour/findByStatus', methods=['GET'])
def find_tour_by_status():
    args = request.args
    tour_status = args.get('tour_status')
    tours = session.query(Tour).filter(Tour.is_available == tour_status)
    return json.dumps([i.to_dict() for i in tours])


@app.route('/tour', methods=['DELETE'])
def delete_tour():
    args = request.args
    tour_id = args.get('tour_id')
    tour = session.query(Tour).filter(Tour.id == tour_id)[0].to_dict()
    session.query(Tour).filter(Tour.id == tour_id).delete()
    session.commit()
    return tour


'''queries dealing with orders'''


@app.route('/order', methods=['POST'])
def create_order():
    args = request.get_json()
    new_order = Order(**args)
    session.add(new_order)
    session.commit()
    return new_order.to_dict()


@app.route('/order', methods=["PUT"])
def update_order():
    args = request.args
    order_id = args.get("order_id")
    args = request.get_json()
    session.query(Order).filter(Order.id == order_id).update(args)
    session.commit()
    order = session.query(Order).filter(Order.id == order_id)[0].to_dict()
    return order


@app.route('/order/findAll', methods=['GET'])
def find_all_orders():
    orders = session.query(Order)
    return json.dumps([i.to_dict() for i in orders])


@app.route('/order/findByID', methods=['GET'])
def find_order_by_id():
    args = request.args
    order_id = args.get('order_id')
    orders = session.query(Order).filter(Order.id == order_id)
    return json.dumps([i.to_dict() for i in orders])


@app.route('/order/findByUsername', methods=['GET'])
def find_order_by_username():
    args = request.args
    username_u = args.get('username')
    orders = session.query(Order).filter(Order.user_id == User.id, User.username == username_u)
    return json.dumps([i.to_dict() for i in orders])


@app.route('/order/findByUserID', methods=['GET'])
def find_order_by_user_id():
    args = request.args
    user_id = args.get('user_id')
    orders = session.query(User).filter(User.id == user_id)
    return json.dumps([i.to_dict() for i in orders])


@app.route('/order', methods=['DELETE'])
def delete_order():
    args = request.args
    order_id = args.get('order_id')
    order = session.query(Order).filter(Order.id == order_id)[0].to_dict()
    session.query(Order).filter(Order.id == order_id).delete()
    session.commit()
    return order


'''queries dealing with users'''


@app.route('/user', methods=['POST'])
def create_user():
    args = request.get_json()
    new_user = User(**args)
    session.add(new_user)
    session.commit()
    return new_user.to_dict()


@app.route('/user', methods=['PUT'])
def update_user():
    args = request.args
    user_id = args.get("user_id")
    args = request.get_json()
    session.query(User).filter(User.id == user_id).update(args)
    session.commit()
    user = session.query(User).filter(User.id == user_id)[0].to_dict()
    return user


@app.route('/user/login', methods=['GET'])
def login():
    pass


@app.route('/user/logout', methods=['GET'])
def logout():
    pass


@app.route('/user/findUserByUsername', methods=['GET'])
def find_user_by_username():
    args = request.args
    username1 = args.get('username')
    users = session.query(User).filter(User.username == username1)
    return json.dumps([i.to_dict() for i in users])


@app.route('/user/findAll', methods=['GET'])
def find_all_users():
    users = session.query(User)
    return json.dumps([i.to_dict() for i in users])


@app.route('/user', methods=['DELETE'])
def delete_user():
    args = request.args
    user_id = args.get('user_id')
    user = session.query(User).filter(User.id == user_id)[0].to_dict()
    session.query(User).filter(User.id == user_id).delete()
    session.commit()
    return user
