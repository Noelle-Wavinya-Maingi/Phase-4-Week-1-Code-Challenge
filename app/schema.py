from app import ma
from app.models import Restaurant, Pizza, RestaurantPizza

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
