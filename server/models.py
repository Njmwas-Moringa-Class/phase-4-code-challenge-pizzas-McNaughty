from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    # Add relationship to RestaurantPizza
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='restaurant')

    def serialize(self, recursion_depth=1):
        if recursion_depth <= 0:
            return {'id': self.id, 'name':self.name}
        else:
            return {
                'id': self.id,
                'name': self.name,
                'address': self.address,
                'restaurant_pizzas': [rp.serialize(recursion_depth - 1) for rp in self.restaurant_pizzas]
            }

    def __repr__(self):
        return f'<Restaurant {self.name}>'

class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # Add relationship to RestaurantPizza
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='pizza')

    def serialize(self, recursion_depth=1):
        if recursion_depth <= 0:
            return {'id': self.id, 'name': self.name}
        else:
            return{
                'id': self.id,
                'name': self.name,
                'ingredients': self.ingredients,
                'restaurant_pizzas': [rp.serialize(recursion_depth - 1) for rp in self.restaurant_pizzas]
            }

    def __repr__(self):
        return f'<Pizza {self.name}, {self.ingredients}>'

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # Add relationships
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

    @validates('price')
    def validate_price(self, key, price):
        if price == 0:
            raise ValueError("Price cannot be zero.")
        elif not 1 <= price <= 30:
            raise ValueError("Price must be between 1 and 30.")
        return price

    def serialize(self, recursion_depth=1):
        if recursion_depth <= 0:
            return {'id': self.id, 'price': self.price}
        else:
            return {
                'id': self.id,
                'price': self.price,
                'pizza_id': self.pizza_id,
                'restaurant_id': self.restaurant_id
            }

    def __repr__(self):
        return f'<RestaurantPizza ${self.price}>'

