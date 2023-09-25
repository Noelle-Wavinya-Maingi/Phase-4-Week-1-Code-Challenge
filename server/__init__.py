from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_marshmallow import Marshmallow

# Create a Flask application
app = Flask(__name__)
api = Api(app)
ma = Marshmallow(app)

# Configure the database URI and disable modification tracking
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Initialize database and migration
migrate = Migrate(app, db)

from server import routes