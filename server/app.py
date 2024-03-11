#!/usr/bin/env python3

from codecs import replace_errors
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
# from flask_restful import Api, Resource
import os

from flask import jsonify, abort
# from models import db, Restaurant, RestaurantPizza, Pizza



BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return '<h1>Code challenge</h1>'


@app.route('/restaurants')
def restaurants():
    restaurants = []
    for restaurant in Restaurant.query.all():
        restaurant_dict ={
        "id": restaurant.id,
        "name": restaurant.name,
        "address": restaurant.address,
        
        }

        restaurants.append(restaurant_dict)

    response = make_response(
        jsonify(restaurants),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response



@app.route('/restaurants/<int:id>', methods=['GET'])
def restaurant_by_id(id):
    restaurant = Restaurant.query.filter_by(id=id).first()

    if restaurant is None:
        return jsonify({"error": "Restaurant not found"}), 404

    if request.method == 'GET':
        restaurant_dict = restaurant.to_dict()

        response = make_response(
            jsonify(restaurant_dict),
            200
        )

        response.headers["Content-Type"] = "application/json"

        return response
    
@app.route('/restaurants/<int:restaurant_id>', methods=['DELETE'])
def delete_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    else:
        return jsonify({"error": "Restaurant not found"}), 404

@app.route('/pizzas')
def pizzas():
    pizzas = []
    for pizza in Pizza.query.all():
        pizza_dict ={
        "id": pizza.id,
        "name": pizza.name,
        "ingredients": pizza.ingredients,
        
        }

        pizzas.append(pizza_dict)

    response = make_response(
        jsonify(pizzas),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response

# @app.route('/restaurant_pizzas', methods=['GET'])
# def restaurant_pizzas():
#     restaurantPizzas = []
#     for r_pizza in RestaurantPizza.query.all():
#         restaurant_pizzas_dict = r_pizza.to_dict()
#         restaurantPizzas.append(restaurant_pizzas_dict)

#     response = make_response(
#             jsonify(restaurantPizzas),
#             200
#         )

#     response.headers["Content-Type"] = "application/json"

#     return response


# @app.route('/restaurant_pizzas', methods=['POST'])
# def get_restaurant_pizzas():
#         data = request.json
#         # Validating request data
#         if 'price' not in data or 'pizza_id' not in data or 'restaurant_id' not in data:
#             return jsonify({"errors": ["price, pizza_id, and restaurant_id are required"]}), 400

#         price = data['price']
#         pizza_id = data['pizza_id']
#         restaurant_id = data['restaurant_id']

#         # Checking to see if Pizza and Restaurant exist
#         pizza = Pizza.query.get(pizza_id)
#         restaurant = Restaurant.query.get(restaurant_id)
#         if pizza is None:
#             return jsonify({"errors": ["Pizza not found"]}), 404
#         if restaurant is None:
#             return jsonify({"errors": ["Restaurant not found"]}), 404

#         try:
#             # Attempt to create and save the RestaurantPizza
#             restaurant_pizza = RestaurantPizza(price=price, pizza=pizza, restaurant=restaurant)
#             db.session.add(restaurant_pizza)
#             db.session.commit()

#             # Prepare response data
#             response_data = {
#                 "id": restaurant_pizza.id,
#                 "pizza": {
#                     "id": pizza.id,
#                     "name": pizza.name,
#                     "ingredients": pizza.ingredients
#                 },
#                 "pizza_id": pizza.id,
#                 "price": restaurant_pizza.price,
#                 "restaurant": {
#                     "address": restaurant.address,
#                     "id": restaurant.id,
#                     "name": restaurant.name
#                 },
#                 "restaurant_id": restaurant.id
#             }

#             return jsonify(response_data), 201
#         except ValueError as e:
#             return jsonify({"error": str(e)}), 400


@app.route('/restaurant_pizzas', methods=['GET', 'POST'])
def restaurant_pizzas():
    if request.method == 'GET':
        restaurantPizzas = []
        for r_pizza in RestaurantPizza.query.all():
            restaurant_pizzas_dict = r_pizza.to_dict()
            restaurantPizzas.append(restaurant_pizzas_dict)

        response = make_response(
            jsonify(restaurantPizzas),
            200
        )

        response.headers["Content-Type"] = "application/json"

        return response

    elif request.method == 'POST':
        data = request.json

        # Validating request data
        if 'price' not in data or 'pizza_id' not in data or 'restaurant_id' not in data:
            return jsonify({"errors": ["price, pizza_id, and restaurant_id are required"]}), 400

        price = data['price']
        pizza_id = data['pizza_id']
        restaurant_id = data['restaurant_id']

        # Checking to see if Pizza and Restaurant exist
        pizza = Pizza.query.get(pizza_id)
        restaurant = Restaurant.query.get(restaurant_id)
        if pizza is None:
            return jsonify({"errors": ["Pizza not found"]}), 404
        if restaurant is None:
            return jsonify({"errors": ["Restaurant not found"]}), 404

        try:
            # Attempt to create and save the RestaurantPizza
            restaurant_pizza = RestaurantPizza(price=price, pizza=pizza, restaurant=restaurant)
            db.session.add(restaurant_pizza)
            db.session.commit()

            # Prepare response data
            response_data = {
                "id": restaurant_pizza.id,
                "price": restaurant_pizza.price,
                "pizza": {
                    "id": pizza.id,
                    "name": pizza.name,
                    "ingredients": pizza.ingredients
                },
                "pizza_id": pizza.id,
                "restaurant": {
                    "id": restaurant.id,
                    "name": restaurant.name,
                    "address": restaurant.address
                },
                "restaurant_id": restaurant.id
            }

            return jsonify(response_data), 201
        
        except ValueError as e:
            return jsonify({"errors": ["validation errors"]}), 400


    
if __name__ == '__main__':
    app.run(port=5555, debug=True)