from flask import request, Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import *
import json
from flask_bcrypt import generate_password_hash

app = Flask(__name__)
from flask_marshmallow import *
from marshmallow import Schema, post_load, ValidationError, validate

Session = sessionmaker(bind=engine)
session = Session()
'''queries dealing with tours table'''


@app.route('/tour', methods=['PUT'])
def update_tour():
    arg = request.args

    # if  ["name", "price", "photoUrl", "is_available"]:
    #     return {"message": "Incorrect input"}, 400
    try:
        tour_id = arg.get("tour_id")
        if not validate_entry_id(Tour, tour_id):
            return {"message": "Tour with such id does not exist"}, 404
        else:
            args = request.get_json()
            tour_schema = TourSchema()
            tour_check = tour_schema.load(args, session=session)
            session.query(Tour).filter(Tour.id == tour_id).update(args)
            session.commit()
            new_tour = session.query(Tour).filter(Tour.id == tour_id).one()
            return tour_schema.dump(new_tour), 200
    except ValidationError as err:
        # return str(err)
        return {"message": "Not correct data provided"}, 400


@app.route('/tour', methods=['POST'])
def create_tour():
    args = request.get_json()
    try:
        tour_schema = TourSchema()
        tour = tour_schema.load(args, session=session)
        session.add(tour)
        session.commit()
        return tour_schema.dump(tour)
    except ValidationError:
        return {"message": "Not correct data provided"}, 400


@app.route('/tour/findAll', methods=['GET'])
def find_all_tours():
    tours = session.query(Tour)
    return json.dumps([i.to_dict() for i in tours]), 200


@app.route('/tour/findByID/<int:tour_id>', methods=['GET'])
def find_tour_by_id(tour_id):
    # args = request.args
    if validate_entry_id(Tour, tour_id):
        tour = session.query(Tour).filter(Tour.id == tour_id).first()
        tour_schema = TourSchema()
        return tour_schema.dump(tour), 200
    return {"message": "Tour with such id does not exist"}, 404


@app.route('/tour/findByStatus', methods=['GET'])
def find_tour_by_status():
    args = request.args
    tour_status = args.get('tour_status')
    if tour_status != '0' and tour_status != "1":
        return {"message": "Not correct status"}, 400
    else:
        tours = session.query(Tour).filter(Tour.is_available == tour_status)
        tour_schema = TourSchema()
        return f"{[tour_schema.dump(i) for i in tours]}", 200


@app.route('/tour/<int:tour_id>', methods=['DELETE'])
def delete_tour(tour_id):
    # args = request.args
    # tour_id = args.get('tour_id')
    if validate_entry_id(Tour, tour_id):
        # return {"message": "Tour with such id does not exist"}, 400
        session.query(Order).filter(Order.tour_id == tour_id).delete()
        session.query(Tour).filter(Tour.id == tour_id).delete()
        session.commit()
        return {"message": "Tour deleted successfully"}, 200
    return {"message": "Tour with such id does not exist"}, 404




'''queries dealing with orders'''


@app.route('/order', methods=['POST'])
def create_order():
    args = request.get_json()
    try:
        order_schema = OrderSchema()
        order = order_schema.load(args, session=session)
        if validate_entry_id(Tour, order.tour_id) and validate_entry_id(User, order.user_id):
            session.add(order)
            session.commit()
            return order_schema.dump(order), 200
        else:
            return {"message": "Some of provided ids does not exist"}, 404
    except ValidationError as err:
        return {"message": "Not correct data provided"}, 400


@app.route('/order', methods=["PUT"])
def update_order():
    arg = request.args
    try:
        order_id = arg.get("order_id")
        if not validate_entry_id(Order, order_id):
            return {"message": "Order with such id does not exist"}, 404
        else:
            args = request.get_json()
            order_schema = OrderSchema()
            updated_order = order_schema.load(args, session=session)
            if validate_entry_id(Tour, updated_order.tour_id) and validate_entry_id(User, updated_order.user_id):
                if validate_order_status(updated_order.status):
                    session.query(Order).filter(Order.id == order_id).update(args)
                    session.commit()
                    new_order = session.query(Order).filter(Order.id == order_id).one()
                    return order_schema.dump(new_order), 200
            return {"message": "Some of provided ids does not exist"}, 404
    except ValidationError as err:
        # return str(err)
        return {"message": "Not correct data provided"}, 400


@app.route('/order/findAll', methods=['GET'])
def find_all_orders():
    orders = session.query(Order)
    return json.dumps([i.to_dict() for i in orders])


@app.route('/order/findByID/<int:order_id>', methods=['GET'])
def find_order_by_id(order_id):
    # args = request.args
    # order_id = args.get('order_id')
    if validate_entry_id(Order, order_id):
        order = session.query(Order).filter(Order.id == order_id).first()
        order_schema = OrderSchema()
        return order_schema.dump(order), 200
    return {"message": "Order with such id does not exist"}, 404


@app.route('/order/findByUserID', methods=['GET'])
def find_order_by_user_id():
    args = request.args
    user_id = args.get('user_id')
    if session.query(Order).filter(Order.user_id == user_id).count() == 0:
        return {"message": "User with this id does not have any orders"}, 200
    if validate_entry_id(User, user_id):
        orders = session.query(Order).filter(Order.user_id == user_id and User.id == user_id)
        order_schema = OrderSchema()
        return f'{[order_schema.dump(i) for i in orders]}', 200
    return {"message": "User with such id does not exist"}, 404


@app.route('/order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    try:
        if validate_entry_id(Order, order_id):
            session.query(Order).filter(Order.id == order_id).delete()
            session.commit()
            return {"message": "Order deleted successfully"}, 200
    except ValidationError:
        return {"message": "Invalid input"}, 400
    return {"message": "Order with such id does not exist"}, 404


'''queries dealing with users'''


@app.route('/user', methods=['POST'])
def create_user():
    args = request.get_json()
    try:
        user_schema = UserSchema()
        user = user_schema.load(args, session=session)
        user.password = generate_password_hash(user.password)
        session.add(user)
        session.commit()
        return user_schema.dump(user), 200
    except ValidationError as err:
        return {"message": "Not correct data provided"}, 400


@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        if not validate_entry_id(User, user_id):
            return {"message": "User with such id does not exist"}, 404
        else:
            args = request.get_json()
            user_schema = UserSchema()
            user1 = user_schema.load(args, session=session)
            session.query(User).filter(User.id == user_id).update(args)

            session.commit()
            user = session.query(User).filter(User.id == user_id).one().to_dict()
            return user_schema.dump(user), 200
    except ValidationError as err:
        return jsonify(err.messages), 400


@app.route('/user/login', methods=['GET'])
def login():
    pass


@app.route('/user/logout', methods=['GET'])
def logout():
    pass


@app.route('/user/findUserByUsername', methods=['GET'])
def find_user_by_username():
    args = request.args
    username = args.get("username")
    if session.query(User).filter(User.username == username) != 0:
        users = session.query(User).filter(User.username == username)
        user_schema = UserSchema()
        return f"{[user_schema.dump(i) for i in users]}", 200
    return {"message": "User with such id does not exist"}, 404



@app.route('/user/findUserByID/<int:user_id>', methods=['GET'])
def find_user_by_id(user_id):
    if validate_entry_id(User, user_id):
        user = session.query(User).filter(User.id == user_id).first()
        user_schema = UserSchema()
        return user_schema.dump(user), 200
    return {"message": "User with such id does not exist"}, 404


@app.route('/user/findAll', methods=['GET'])
def find_all_users():
    users = session.query(User)
    return json.dumps([i.to_dict() for i in users])


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # args = request.args
    # tour_id = args.get('tour_id')
    if validate_entry_id(User, user_id):
        # return {"message": "Tour with such id does not exist"}, 400
        session.query(Order).filter(Order.user_id == user_id).delete()
        session.query(User).filter(User.id == user_id).delete()
        session.commit()
        return {"message": "User deleted successfully"}, 200
    return {"message": "User with such id does not exist"}, 404
