#!/usr/bin/env python3

from models import db, Customer, Coffee, Order
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db, render_as_batch=True)

db.init_app(app)
api = Api(app)


class Home(Resource):
    def get(self):
        response_dict = {
            'message': 'Coffee Shop Practice Challenge'
        }
        return make_response(response_dict, 200, )

api.add_resource(Home, '/')

class Coffees(Resource):
    def get(self):
        coffees = [c.to_dict(only=('id', 'name')) for c in Coffee.query.all()] 
        return make_response(coffees, 200)

api.add_resource(Coffees, '/coffees')

class CoffeeByID(Resource):
    def get(self, id):
        coffee = Coffee.query.get(id)
        if not coffee:
            return make_response({'error': 'coffee not found.'})
        return make_response(coffee.to_dict(), 200)

    def delete(self, id):
        coffee = Coffee.query.get(id)
        if not coffee:
            return make_response({'error': 'Coffee not found'})
        db.session.delete(coffee)
        db.session.commit()
        return make_response('', 204)

api.add_resource(CoffeeByID, '/coffees/<int:id>')

class Customers(Resource):
    def get(self):
        customers = [c.to_dict(only=('id', 'name')) for c in Customer.query.all()]
        return make_response(customers, 200)

api.add_resource(Customers, '/customers')

class CustomersById(Resource):
    def get(self, id):
        customer = Customer.query.get(id)
        if not customer:
            return make_response({'error': 'Customer not found.'})

api.add_resource(CustomersById, '/customers/<int:id>')

class Orders(Resource):
    def get(self):
        orders = [o.to_dict() for o in Order.query.all()]
        return make_response(orders, 200)
    
    def post(self):
        params = request.json
        try:
            order = Order(coffee_id=params['coffee_id'], customer_id=params['customer_id'],price=params['price'], customization=params['customization'])
        except ValueError as v_error:
            return make_response({'error': [str(v_error)]}, 422)
        db.session.add(order)
        db.session.commit()
        return make_response(order.to_dict(), 201)
api.add_resource(Orders, '/orders')



if __name__ == '__main__':
    app.run(port=5555, debug=True)
