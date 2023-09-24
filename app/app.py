# Import necessary modules and classes
from flask import Flask, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Restaurant
from flask_marshmallow import Marshmallow

# Create a Flask application
app = Flask(__name__)

# Configure the database URI and disable modification tracking
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database and migration
migrate = Migrate(app, db)
db.init_app(app)

# Initialize Marshmallow for serialization/deserialization
ma = Marshmallow(app)

# Create a Marshmallow schema for the Restaurant model
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

# Entry point of the application
if __name__ == "__main__":
    app.run(port=5555)
