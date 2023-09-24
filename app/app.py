# Import necessary modules and classes
from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Restaurant, Pizza, RestaurantPizza
from flask_marshmallow import Marshmallow

# Create a Flask application
app = Flask(__name__)

# Configure the database URI and disable modification tracking
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database and migration
migrate = Migrate(app, db)
db.init_app(app)

# Initialize Marshmallow for serialization
ma = Marshmallow(app)


class RestaurantSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Restaurant

    id = ma.auto_field()
    name = ma.auto_field()
    address = ma.auto_field()


# Create instances of the Restaurant schema for single and multiple objects
restaurant_schema = RestaurantSchema()
restaurants_schema = RestaurantSchema(many=True)


class PizzaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Pizza

    id = ma.auto_field()
    name = ma.auto_field()
    ingredients = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()


# Create instances of the Pizza schema for single and multiple objects
pizza_schema = PizzaSchema()
pizzas_schema = PizzaSchema(many=True)


class RestaurantPizzaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = RestaurantPizza

    id = ma.auto_field()
    pizza_id = ma.auto_field()
    restaurant_id = ma.auto_field()
    price = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()


# Create instances of the Pizza schema for single and multiple objects
restaurantpizza_schema = RestaurantPizzaSchema()
restaurantpizzas_schema = RestaurantPizzaSchema(many=True)


# Initialize Flask-RESTful API
api = Api(app)


# Define a Resource for the home route ("/")
class Home(Resource):
    def get(self):
        # Create a response dictionary
        response_dict = {"home": "Welcome to the Restaurant API."}

        # Create an HTTP response with the dictionary and status code 200 (OK)
        response = make_response(response_dict, 200)

        return response


# Add the Home resource to handle the root ("/") route
api.add_resource(Home, "/")


# Define a Resource for the "/restaurants" route
class Restaurants(Resource):
    def get(self):
        # Retrieve all restaurants from the database
        restaurants = Restaurant.query.all()
        # Serialize the restaurants using the schema
        response = make_response(restaurants_schema.dump(restaurants), 200)

        return response


# Add the Restaurants resource to handle the "/restaurants" route
api.add_resource(Restaurants, "/restaurants")


# Define a Resource for the "/restaurants/<int:id>" route
class RestaurantByID(Resource):
    def get(self, id):
        # Retrieve a single restaurant by its ID
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            # Serialize the restaurant using the schema for a single object
            response = make_response(restaurant_schema.dump(restaurant), 200)
        else:
            # If the restaurant with the specified ID doesn't exist, return a 404 response
            response_dict = {"error": "Restaurant not found"}
            response = make_response(response_dict, 404)

        return response

    def delete(self, id):
        try:
            restaurant = Restaurant.query.filter_by(id=id).first()

            if restaurant:
                # Delete associated records in the RestaurantPizza
                RestaurantPizza.query.filter_by(restaurant_id=id).delete()

                # Delete the restaurant from the database
                db.session.delete(restaurant)
                db.session.commit()

                response_dict = {"Message": "Restaurant deleted successfully!"}

                response = make_response(response_dict, 200)

            else:
                response_dict = {"error": "Restaurant not found!"}

                response = make_response(response_dict, 404)

        except Exception as e:
            # Handle any exceptions that may occur during the deletion process
            response_dict = {"error": str(e)}

            response = make_response(response_dict, 500)

        return response


# Add the RestaurantByID resource to handle the "/restaurants/<int:id>" route
api.add_resource(RestaurantByID, "/restaurants/<int:id>")


class Pizzas(Resource):
    def get(self):
        # Retrieve all pizzas from the database
        pizza = Pizza.query.all()
        # Serialize the pizzas using the schema
        response = make_response(pizzas_schema.dump(pizza), 200)

        return response


# Add the Pizzas resource to handle the "/pizzas" route
api.add_resource(Pizzas, "/pizzas")


class PizzaByID(Resource):
    def get(self, id):
        response_dict = Pizza.query.filter_by(id=id).first()

        response = make_response(pizza_schema.dump(response_dict), 200)

        return response

    def delete(self, id):
        try:
            pizza = Pizza.query.filter_by(id=id).first()

            if pizza:
                # Delete associated records in the RestaurantPizza
                RestaurantPizza.query.filter_by(pizza_id=id).delete()

                # Delete the pizza from the database
                db.session.delete(pizza)
                db.session.commit()

                response_dict = {"Message": "Pizza deleted successfully!"}

                response = make_response(response_dict, 200)

            else:
                response_dict = {"error": "Pizza not found!"}

                response = make_response(response_dict, 404)

        except Exception as e:
            response_dict = {"error": str(e)}

            response = make_response(response_dict, 500)

        return response


# Add the PizzaByID resource to handle the "/pizzas/<int:id>" route
api.add_resource(PizzaByID, "/pizzas/<int:id>")


class RestaurantPizzas(Resource):
    def get(self):
        restaurantpizza = RestaurantPizza.query.all()

        response = make_response(restaurantpizzas_schema.dump(restaurantpizza), 200)

        return response

    def post(self):
        try:
            # Parse the JSON data from the request body
            price = float(request.form.get("price"))
            pizza_name = request.form.get("pizza_name")
            restaurant_name = request.form.get("restaurant_name")

            # Retrieve the associated Pizza and Restaurant by name
            pizza = Pizza.query.filter_by(name=pizza_name).first()
            restaurant = Restaurant.query.filter_by(name=restaurant_name).first()

            # Check if the Pizza and Restaurant exist
            if not pizza or not restaurant:
                response_dict = {"errors": ["Pizza or Restaurant not found"]}
                return make_response(jsonify(response_dict), 404)

            # Create a new RestaurantPizza instance
            restaurant_pizza = RestaurantPizza(
                pizza=pizza, restaurant=restaurant, price=price
            )

            # Add and commit the new RestaurantPizza to the database
            db.session.add(restaurant_pizza)
            db.session.commit()

            # Serialize and return the associated Pizza data
            response_dict = {
                "message": "Restaurant_pizza created for...",
                "pizza": {
                    "id": pizza.id,
                    "name": pizza.name,
                    "ingredients": pizza.ingredients,
                },
                "restaurant": {
                    "id": restaurant.id,
                    "name": restaurant.name,
                    "address": restaurant.address,
                },
                "price": restaurant_pizza.price,
            }

            response = make_response(jsonify(response_dict), 200)

        except Exception as e:
            # Handle any exceptions that may occur during the creation process
            response_dict = {"errors": ["An error occurred"]}
            return make_response(jsonify(response_dict), 500)

        return response


# Add the RestaurantPizza resource to handle the route '/restaurantspizza'
api.add_resource(RestaurantPizzas, "/restaurantspizza")

# Entry point of the application
if __name__ == "__main__":
    app.run(port=5555)
