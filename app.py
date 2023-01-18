from flask import Flask
from api_lib.app_config import configure_app


def create_app(db_url=None, jwt_secret_key=None):
    app = Flask(__name__)
    configure_app(app=app, db_url=db_url, jwt_secret_key=jwt_secret_key)

    return app
