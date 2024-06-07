from datetime import timedelta
import os

from flask import Flask
from decouple import config
from db import db
from . import auth, home
from flask_jwt_extended import JWTManager


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Check if the environment variable for the database URL is set
    database_url = config("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set.")
    app.config.from_mapping(
        SECRET_KEY=config("SECRET_KEY"),
        DATABASE=database_url,
        JWT_SECRET_KEY=config("JWT_SECRET_KEY"),
        OPEN_WEATHER_KEY=config("OPEN_WEATHER_KEY"),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1),
        JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize the database connection
    db.init_app(app)

    # Embed the JWT extension
    JWTManager(app)

    # register all blueprin routes
    app.register_blueprint(auth.bp)
    app.register_blueprint(home.bp)

    return app
