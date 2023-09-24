from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Restaurant(db.Model):
    __tablename__ = "Restaurant"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String, nullable=False)

    pizzas = db.relationship(
        "Pizza", secondary="restaurant_pizzas", backref="Restaurant"
    )

    def __repr__(self):
        return f"{self.name} {self.address}"


class Pizza(db.Model):
    __tablename__ = "Pizza"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    ingredients = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    restaurants = db.relationship(
        "Restaurant", secondary="restaurant_pizzas", backref="Pizza"
    )

    def __repr__(self):
        return f"{self.name} {self.ingredients} {self.created_at} {self.updated_at}"


class RestaurantPizza(db.Model):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    restaurant_id = db.Column(
        db.Integer, db.ForeignKey("Restaurant.id"), nullable=False
    )
    restaurant = db.relationship(
        "Restaurant", backref=db.backref("restaurant_pizzas", lazy=True)
    )

    pizza_id = db.Column(db.Integer, db.ForeignKey("Pizza.id"), nullable=False)
    pizza = db.relationship("Pizza", backref=db.backref("restaurant_pizzas", lazy=True))

    def __repr__(self):
        return f"<RestaurantPizza {self.restaurant.name} - {self.pizza.name}>"
