from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from dotenv import load_dotenv
from resources import tags_blueprint, item_blueprint, store_blueprint, users_blueprint
from api_lib.db import db
from api_lib.tokens import create_jwt_manager

import os


def configure_app(app: Flask, *args, **kwargs):
    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Simple Store API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = kwargs['db_url'] or os.getenv(key="DATABASE_URL", default="sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = kwargs['jwt_secret_key'] or os.getenv(key="JWT_SECRET_KEY", default="momma")

    api = Api(app=app)

    api.register_blueprint(blp=store_blueprint)
    api.register_blueprint(blp=item_blueprint)
    api.register_blueprint(blp=tags_blueprint)
    api.register_blueprint(blp=users_blueprint)

    db.init_app(app=app)
    migrate = Migrate(app=app, db=db)
    jwt = create_jwt_manager(app=app)

    # with app.app_context():
    #     db.create_all()
