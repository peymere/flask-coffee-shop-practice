#!/usr/bin/env python3

from app import app
from models import db, Customer, Coffee, Order

with app.app_context():

    # This will delete any existing rows
    # so you can run the seed file multiple times without having duplicate entries in your database
    print("Deleting data...")
    Customer.query.delete()
    Coffee.query.delete()
    Order.query.delete()

    print("Creating Customers...")
    karen = Customer(name="Karen")
    sanjay = Customer(name="Sanjay")
    kiki = Customer(name="Kiki")
    customers = [karen, sanjay, kiki]

    print("Creating Coffees...")

    c1 = Coffee(name="Mocha")
    c2 = Coffee(name="Latte")
    c3 = Coffee(name="Flat White")
    coffees = [c1, c2, c3]

    print("Creating Orders...")

    o1 = Order(customer=karen, coffee=c1, price=5, customization="iced")
    o2 = Order(customer=sanjay, coffee=c2, price=4, customization="oat milk")
    o3 = Order(customer=kiki, coffee=c3, price=5, customization="almond milk")
    o4 = Order(customer=kiki, coffee=c1, price=5, customization="almond milk")
    o5 = Order(customer=sanjay, coffee=c2, price=4, customization="iced, oat milk")
    o6 = Order(customer=kiki, coffee=c3, price=5, customization="almond milk")
    orders = [o1, o2, o3, o4, o5, o6]

    db.session.add_all(coffees)
    db.session.add_all(customers)
    db.session.add_all(orders)
    db.session.commit()

    print("Seeding done!")