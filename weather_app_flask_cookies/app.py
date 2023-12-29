from dotenv import dotenv_values
from flask import Flask
from weather_app_flask_cookies.routes import main

config = dotenv_values(".env")


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config["SECRET_KEY"]

    app.register_blueprint(main)
    return app
