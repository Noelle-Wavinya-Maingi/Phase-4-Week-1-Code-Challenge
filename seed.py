from server.models import Restaurant, Pizza, RestaurantPizza
from server import db,app


with app.app_context():
    # Create restaurants
    restaurant1 = Restaurant(name="Restaurant 1", address="123 Main St")
    restaurant2 = Restaurant(name="Restaurant 2", address="456 Elm St")
    restaurant3 = Restaurant(name="Restaurant 3", address="789 Oak St")

    # Create pizzas
    pizza1 = Pizza(name="Pizza 1", ingredients="Cheese, Tomato Sauce, Pepperoni")
    pizza2 = Pizza(name="Pizza 2", ingredients="Cheese, Tomato Sauce, Mushrooms")
    pizza3 = Pizza(name="Pizza 3", ingredients="Cheese, Tomato Sauce, Sausage")

    # Create restaurant_pizzas associations with prices
    rp1 = RestaurantPizza(restaurant=restaurant1, pizza=pizza1, price=12)
    rp2 = RestaurantPizza(restaurant=restaurant1, pizza=pizza2, price=14)
    rp3 = RestaurantPizza(restaurant=restaurant2, pizza=pizza2, price=13)
    rp4 = RestaurantPizza(restaurant=restaurant2, pizza=pizza3, price=15)
    rp5 = RestaurantPizza(restaurant=restaurant3, pizza=pizza1, price=11)

# Add objects to the session and commit to the database
    db.session.add_all([restaurant1, restaurant2, restaurant3, pizza1, pizza2, pizza3, rp1, rp2, rp3, rp4, rp5])
    db.session.commit()

print("Data seeded successfully.")
