from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required

from api_lib.schemas import ItemSchema, ItemUpdateSchema
from api_lib.messages import ItemMessages as im
from models import ItemsModel

bp = Blueprint(name="items", import_name=__name__, description="Operations on items")


@bp.route(rule="/items")
class ItemMethods(MethodView):
    @bp.response(status_code=200, schema=ItemSchema(many=True))
    def get(self):
        return ItemsModel.get_all()

    @jwt_required()
    @bp.arguments(schema=ItemSchema)
    @bp.response(status_code=201, schema=ItemSchema)
    def post(self, item_data):
        new_item: ItemsModel = ItemsModel(**item_data)
        new_item.save_to_db()
        return new_item


@bp.route(rule="/items/<int:item_id>")
class ItemByIDMethods(MethodView):
    @bp.response(status_code=200, schema=ItemSchema)
    def get(self, item_id):
        return ItemsModel.find_by_id(item_id)

    @jwt_required()
    def delete(self, item_id):
        item = ItemsModel.find_by_id(item_id)
        item.delete_from_db()
        return im.item_deleted_msg(item.name, item.id)

    @jwt_required()
    @bp.arguments(schema=ItemUpdateSchema)
    @bp.response(status_code=200, schema=ItemUpdateSchema)
    def put(self, item_data, item_id):
        item = ItemsModel.find_by_id(item_id)

        if item:
            item.name = item_data['name']
            item.price = item_data['price']
        else:
            item = ItemsModel(id=item_id, **item_data)

        item.save_to_db()
        return item
