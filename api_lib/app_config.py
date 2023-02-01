from flask import Flask, request
from flask_babel import Babel
from flask_smorest import Api
from flask_migrate import Migrate
from dotenv import load_dotenv
from resources import Api_Blueprints as ab
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
    app.config["BABEL_DEFAULT_LOCALE"] = 'en_US'
    app.config["BABEL_DEFAULT_TIMEZONE"] = 'Asia/Yerevan'
    app.config["LANGUAGES"] = {
        "ru": "Russian",
        "en": "English"
    }

    api = Api(app=app)
    ab.register_all(api=api)

    db.init_app(app=app)
    migrate = Migrate(app=app, db=db)
    jwt = create_jwt_manager(app=app)

    with app.app_context():
        # db.create_all()
        def get_locale():
            return request.accept_languages.best_match(app.config["LANGUAGES"].keys())
        babel = Babel(app=app, locale_selector=get_locale)
