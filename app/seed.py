from random import randint, random, choice as rc
from faker import Faker
from app import app, db
from models import Restaurant, Pizza, RestaurantPizza

fake = Faker()

with app.app_context():

    RestaurantPizza.query.delete()
    Restaurant.query.delete()
    Pizza.query.delete()

    restaurants = []
    for i in range(20):
        r = Restaurant(
            name=fake.company(),
            address=fake.address()
        )
        restaurants.append(r)

    db.session.add_all(restaurants)

    pizzas = []
    pizza_names = []
    for i in range(200):

        name = fake.word()
        while name in pizza_names:
            name = fake.word()
        pizza_names.append(name)

        p = Pizza(
            name=name,
            ingredients=fake.sentence()
        )

        pizzas.append(p)

    db.session.add_all(pizzas)
    db.session.commit()

    restaurant_pizzas = []
    for i in range(400):
        restaurant = rc(restaurants)
        pizza = rc(pizzas)
        price = round(randint(5, 15) + random(), 2)

        rp = RestaurantPizza(
            restaurant=restaurant,
            pizza=pizza,
            price=price
        )

        restaurant_pizzas.append(rp)

    db.session.add_all(restaurant_pizzas)
    db.session.commit()

    most_expensive_pizza = rc(restaurant_pizzas)
    most_expensive_pizza.price = 100
    db.session.add(most_expensive_pizza)
    db.session.commit()
