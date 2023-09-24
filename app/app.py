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
        # Retrieve a single restaurant by ID
        restaurant = Restaurant.query.get(id)
        if restaurant:
            # Delete the restaurant from the database
            db.session.delete(restaurant)
            db.session.commit()
            response_dict = {"message": "Restaurant successfully deleted."}
            return make_response(response_dict, 200)
        else:
            response_dict = {"error": "Restaurant not found!"}
            return make_response(response_dict, 404)


# Add the RestaurantByID resource to handle the "/restaurants/<int:id>" route
api.add_resource(RestaurantByID, "/restaurants/<int:id>")

# Entry point of the application
if __name__ == "__main__":
    app.run(port=5555)
