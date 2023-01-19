from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from api_lib.db import db
from api_lib.schemas import TagSchema, TagsByItemsSchema, PlainTagSchema
from models import TagsModel, ItemsModel, StoresModel

blueprint = Blueprint(name="tags", import_name=__name__, description="Operations on tags")


@blueprint.route("/stores/<int:store_id>/tags")
class TagsInStoreMethods(MethodView):
    @blueprint.response(status_code=200, schema=PlainTagSchema(many=True))
    def get(self, store_id):
        store_exists = db.get_or_404(entity=StoresModel, ident=store_id)
        statement = db.select(TagsModel).where(TagsModel.store_id == store_id)
        return db.session.execute(statement).scalars().all()

    @jwt_required()
    @blueprint.arguments(schema=TagSchema)
    @blueprint.response(status_code=201, schema=TagSchema)
    def post(self, tag_data, store_id):
        new_tag = TagsModel(**tag_data, store_id=store_id)

        statement = db.select(TagsModel) \
                      .where(TagsModel.store_id == store_id) \
                      .where(TagsModel.name == tag_data['name'])

        already_exists = db.session.execute(statement).scalars().all()

        if already_exists:
            abort(http_status_code=409,
                  message=f"duplicate: store_id {store_id} already has tag {new_tag.name}")
        try:
            db.session.add(new_tag)
            db.session.commit()
        except SQLAlchemyError as err:
            abort(http_status_code=500, message=f"{str(err)}")

        return new_tag


@blueprint.route("/tags/<int:tag_id>")
class TagByID(MethodView):
    @blueprint.response(status_code=200, schema=TagSchema)
    def get(self, tag_id):
        return db.get_or_404(entity=TagsModel, ident=tag_id)

    @jwt_required()
    @blueprint.response(status_code=200, description="Removes tag if no item is tagged with it")
    @blueprint.alt_response(status_code=400, description="Tag is still linked to items and will not be deleted")
    def delete(self, tag_id):
        tag = db.get_or_404(entity=TagsModel, ident=tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": f"tag {tag.name} deleted"}

        abort(http_status_code=400, message="Tag is still linked to items and will not be deleted")


@blueprint.route("/items/<int:item_id>/tags/<int:tag_id>")
class LinkUnlinkTags(MethodView):
    @jwt_required()
    @blueprint.response(status_code=201, schema=TagsByItemsSchema)
    def post(self, item_id, tag_id):
        item = ItemsModel.query.get_or_404(item_id)
        tag = TagsModel.query.get_or_404(tag_id)
        item.tags.append(tag)

        if item.store_id != tag.store_id:
            abort(http_status_code=400, message="Tag and item belong to different stores")

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as err:
            abort(http_status_code=500, message=f"Insertion error: {str(err)}")

        return {"message": f"Tag {tag.name} linked to item {item.name}"}

    @jwt_required()
    @blueprint.response(status_code=200, schema=TagsByItemsSchema)
    def delete(self, item_id, tag_id):
        item = ItemsModel.query.get_or_404(item_id)
        tag = TagsModel.query.get_or_404(tag_id)
        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as err:
            abort(http_status_code=500, message=f"Error removing tag from item: {str(err)}")

        return {"message": f"Removed tag {tag.name} from item: {item.name}"}
