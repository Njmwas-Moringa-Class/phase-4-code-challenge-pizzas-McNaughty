#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

from flask import jsonify

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

restaurants =  [
  { "address": "address1", "id": 1, "name": "Karen's Pizza Shack" },
  { "address": "address2", "id": 2, "name": "Sanjay's Pizza"  },
  { "address": "address3", "id": 3,  "name": "Kiki's Pizza"  }
]


@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants', methods=['GET'])
def list_restaurants():
    return  jsonify(restaurants)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
