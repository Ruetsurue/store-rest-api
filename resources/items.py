from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from api_lib.schemas import ItemSchema, ItemUpdateSchema
from api_lib.db import db
from api_lib.msg_templates import DBErrorTemplates as det, EntityInfoTemplates as eit
from models import ItemsModel

ENTITY_TYPE = 'item'
blueprint = Blueprint(name="items", import_name=__name__, description="Operations on items")


@blueprint.route(rule="/items")
class ItemMethods(MethodView):
    @blueprint.response(status_code=200, schema=ItemSchema(many=True))
    def get(self):
        statement = db.select(ItemsModel)
        result = db.session.execute(statement)
        return result.scalars().all()

    @jwt_required()
    @blueprint.arguments(schema=ItemSchema)
    @blueprint.response(status_code=201, schema=ItemSchema)
    def post(self, item_data):
        new_item: ItemsModel = ItemsModel(**item_data)
        try:
            db.session.add(new_item)
            db.session.commit()
        except SQLAlchemyError as err:
            abort(http_status_code=500, message=det.db_insertion_err_msg(ENTITY_TYPE, new_item.name, err=err))

        return new_item


@blueprint.route(rule="/items/<int:item_id>")
class ItemByIDMethods(MethodView):
    @blueprint.response(status_code=200, schema=ItemSchema)
    def get(self, item_id):
        return db.get_or_404(entity=ItemsModel, ident=item_id)

    @jwt_required()
    def delete(self, item_id):
        item: ItemsModel = db.get_or_404(entity=ItemsModel, ident=item_id)
        db.session.delete(item)
        db.session.commit()

        return eit.entity_deleted_msg(ENTITY_TYPE, item.name, item_id, jsonify=True)

    @jwt_required()
    @blueprint.arguments(schema=ItemUpdateSchema)
    @blueprint.response(status_code=200, schema=ItemUpdateSchema)
    def put(self, item_data, item_id):
        item = db.get_or_404(entity=ItemsModel, ident=item_id)

        if item:
            item.name = item_data['name']
            item.price = item_data['price']
        else:
            item = ItemsModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item
