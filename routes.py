from flask import request, Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import *
import json
from flask_bcrypt import generate_password_hash

app = Flask(__name__)
from flask_marshmallow import *
from marshmallow import Schema, fields, post_load, ValidationError, validate

Session = sessionmaker(bind=engine)
session = Session()
'''queries dealing with tours table'''


@app.route('/tour', methods=['PUT'])
def update_tour():
    arg = request.args
    try:
        tour_id = arg.get("tour_id")
        if not validate_entry_id(Tour, tour_id):
            return {"message": "Tour with such id does not exist"}, 400
        else:
            args = request.get_json()
            tour_schema = TourSchema()
            updated_tour = tour_schema.load(args, session=session)
            if 100 < updated_tour.price > 100000:
                raise ValidationError
            session.query(Tour).filter(Tour.id == tour_id).update(args)
            session.commit()
            new_tour = session.query(Tour).filter(Tour.id == tour_id).one().to_dict()
            return tour_schema.dump(new_tour)
    except ValidationError:
        return {"message": "Not correct data provided"}, 405


@app.route('/tour', methods=['POST'])
def create_tour():
    args = request.get_json()
    try:
        tour_schema = TourSchema()
        tour = tour_schema.load(args, session=session)
        session.add(tour)
        session.commit()
        return tour_schema.dump(tour)
    except ValidationError as err:
        return str(err)


@app.route('/tour/findAll', methods=['GET'])
def find_all_tours():
    tours = session.query(Tour)
    return json.dumps([i.to_dict() for i in tours]), 200


@app.route('/tour/findByID', methods=['GET'])
def find_tour_by_id():
    args = request.args
    tour_id = args.get('tour_id')
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
        return {"message": "Not correct status"}, 404
    else:
        tours = session.query(Tour).filter(Tour.is_available == tour_status)
        tour_schema = TourSchema()
        return f"{[tour_schema.dump(i) for i in tours]}", 200


@app.route('/tour', methods=['DELETE'])
def delete_tour():
    args = request.args
    tour_id = args.get('tour_id')
    try:
        if not validate_entry_id(Tour, tour_id):
            return {"message": "Tour with such id does not exist"}, 400
        # session.query(Order).filter(Order.tour_id == Tour.id, Tour.id == tour_id).delete()
        session.query(Tour).filter(Tour.id == tour_id).delete()
        session.commit()
        return {"message": "Tour deleted successfully"}, 200
    except ValidationError:
        return {"message": "Tour with such id does not exist"}, 404




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
    new_user.password = generate_password_hash(new_user.password)
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


# @app.route('/user/findUserByID', methods=['GET'])
# def find_user_by_ID():
#     args = request.args
#     try:
#         user_id = args.get('user_id')
#         users = session.query(User).filter(User.id == user_id)
#     return json.dumps([i.to_dict() for i in users])

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
