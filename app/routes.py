from flask import  make_response, request, jsonify
from flask_restful import  Resource
from app import db ,api
from app.schema import restaurants_schema, restaurant_schema, pizzas_schema, pizza_schema, restaurantpizzas_schema
from app.models import Pizza, Restaurant, RestaurantPizza

# Define a Resource for the home route ("/")
class Home(Resource):
    def get(self):
        # Create a response dictionary
        response_dict = {"home": "Welcome to the Restaurant API."}

        # Create an HTTP response with the dictionary and status code 200 (OK)
        response = make_response(response_dict, 200)

        return response



# Define a Resource for the "/restaurants" route
class Restaurants(Resource):
    def get(self):
        # Retrieve all restaurants from the database
        restaurants = Restaurant.query.all()
        # Serialize the restaurants using the schema
        response = make_response(restaurants_schema.dump(restaurants), 200)

        return response



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


class RestaurantPizzas(Resource):
    def get(self):
        restaurantpizza = RestaurantPizza.query.all()

        response = make_response(restaurantpizzas_schema.dump(restaurantpizza), 200)

        return response

    def post(self):
        try:
            # Parse form data from the request body
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
                pizza_id=pizza.id, restaurant_id=restaurant.id, price=price
            )

            # Add and commit the new RestaurantPizza to the database
            db.session.add(restaurant_pizza)
            db.session.commit()

            # Serialize and return the associated Pizza data
            response_dict = {
                "message": "Restaurant_pizza created successfully",
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

            response = make_response(jsonify(response_dict), 201)  # Use 201 Created status code

        except Exception as e:
            # Handle any exceptions that may occur during the creation process
            response_dict = {"errors": ["An error occurred: " + str(e)]}
            return make_response(jsonify(response_dict), 500)

        return response


# Add the Home resource to handle the root ("/") route
api.add_resource(Home, "/")
# Add the RestaurantPizza resource to handle the route '/restaurantspizza'
api.add_resource(RestaurantPizzas, "/restaurantspizza")
# Add the PizzaByID resource to handle the "/pizzas/<int:id>" route
api.add_resource(PizzaByID, "/pizzas/<int:id>")
# Add the RestaurantByID resource to handle the "/restaurants/<int:id>" route
api.add_resource(RestaurantByID, "/restaurants/<int:id>")
# Add the Restaurants resource to handle the "/restaurants" route
api.add_resource(Restaurants, "/restaurants")


