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



@app.route('/restaurants/<int:id>')
def restaurant_by_id(id):
    restaurant = Restaurant.query.filter_by(id=id).first()
    
    if restaurant is None:
        return jsonify({"error": "Restaurant not found"}), 404
    
    restaurant_dict = restaurant.to_dict()

    response = make_response(
        jsonify(restaurant_dict),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)