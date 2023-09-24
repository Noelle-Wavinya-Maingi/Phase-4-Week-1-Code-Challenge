# Import necessary modules and classes
from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Restaurant, RestaurantPizza
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
class RestaurantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Restaurant


# Initialize Flask-RESTful API
api = Api(app)


# Define a Resource for the home route ("/")
class Home(Resource):
    def get(self):
        # Create a response dictionary
        response_dict = {"home": "Welcome to the Restaurant API."}
        # Create an HTTP response with the dictionary and status code 200 (OK)
        return make_response(response_dict, 200)


# Add the Home resource to handle the root ("/") route
api.add_resource(Home, "/")


# Define a Resource for the "/restaurants" route
class Restaurants(Resource):
    def get(self):
        # Retrieve all restaurants from the database
        restaurants = Restaurant.query.all()
        # Serialize the restaurants using the schema
        restaurant_schema = RestaurantSchema(many=True)
        response_dict = {"restaurants": restaurant_schema.dump(restaurants)}
        return make_response(response_dict, 200)


# Add the Restaurants resource to handle the "/restaurants" route
api.add_resource(Restaurants, "/restaurants")


# Define a Resource for the '/restaurants/<int:id>' route
class RestaurantByID(Resource):
    def get(self, id):
        # Retrieve a single restaurant by ID
        restaurant = Restaurant.query.get(id)
        if restaurant:
            # Serialize the restaurant using the schema for a single object
            restaurant_schema = RestaurantSchema()
            response_dict = {"restaurant": restaurant_schema.dump(restaurant)}
            return make_response(response_dict, 200)
        else:
            # If the restaurant with the specified ID does not exist, return an error and status code 404
            response_dict = {"error": "Restaurant not found!"}
            return make_response(response_dict, 404)

    def delete(self, id):
        # Retrieve a single restaurant by ID
        restaurant = Restaurant.query.get(id)
        if restaurant:
            # Delete associated RestaurantPizza first
            RestaurantPizza.query.filter_by(restaurant_id=id).delete()
            # Then delete the restaurant
            db.session.delete(restaurant)
            db.session.commit()

            response_dict = {"message": "Restaurant successfully deleted."}

            return make_response(response_dict, 204)
        else:
            response_dict = {"error": "Restaurant not found!"}
            return make_response(response_dict, 404)


# Add RestaurantByID resource to handle the route '/restaurants/<int:id>'
api.add_resource(RestaurantByID, "/restaurants/<int:id>")

# Entry point of the application
if __name__ == "__main__":
    app.run(port=5555)
