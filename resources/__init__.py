from flask_smorest import Api

from resources.stores import bp as store_bp
from resources.items import bp as item_bp
from resources.tags import bp as tags_bp
from resources.users import bp as users_bp
from resources.confirmation import bp as confirmation_bp


class Api_Blueprints:
    blueprints = [
        store_bp,
        item_bp,
        tags_bp,
        users_bp,
        confirmation_bp
    ]

    @classmethod
    def register_all(cls, api: Api):
        for bp in cls.blueprints:
            api.register_blueprint(blp=bp)
