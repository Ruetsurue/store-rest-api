from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required

from api_lib.messages import StoreMessages as sm
from api_lib.schemas import StoreSchema
from models import StoresModel

bp = Blueprint(name="stores", import_name=__name__, description="Operations on stores")


@bp.route(rule="/stores")
class StoreMethods(MethodView):
    @bp.response(status_code=200, schema=StoreSchema(many=True))
    def get(self):
        return StoresModel.get_all()

    @jwt_required(fresh=False)
    @bp.arguments(schema=StoreSchema)
    @bp.response(status_code=201, schema=StoreSchema)
    def post(self, store_data):
        new_store = StoresModel(**store_data)
        new_store.save_to_db()
        return new_store


@bp.route(rule="/stores/<int:store_id>")
class StoreByIDMethods(MethodView):
    @bp.response(status_code=200, schema=StoreSchema)
    def get(self, store_id):
        return StoresModel.find_by_id(store_id)

    @jwt_required(fresh=True)
    def delete(self, store_id):
        store = StoresModel.find_by_id(store_id)
        store.delete_from_db()
        return sm.store_deleted_msg(store.name, store.id)
