from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from schemas import ItemSchema, ItemUpdateSchema
from db import db
from models import ItemsModel

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
        new_item = ItemsModel(**item_data)
        try:
            db.session.add(new_item)
            db.session.commit()
        except SQLAlchemyError as err:
            abort(http_status_code=500, message=f"Error inserting items: {err.args}")

        return new_item


@blueprint.route(rule="/items/<int:item_id>")
class ItemByIDMethods(MethodView):
    @blueprint.response(status_code=200, schema=ItemSchema)
    def get(self, item_id):
        return db.get_or_404(entity=ItemsModel, ident=item_id)

    @jwt_required()
    def delete(self, item_id):
        item = db.get_or_404(entity=ItemsModel, ident=item_id)
        db.session.delete(item)
        db.session.commit()

        return {"message": "item deleted"}

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
