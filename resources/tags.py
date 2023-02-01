from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from api_lib.messages import TagMessages as tm
from api_lib.schemas import TagSchema, TagsByItemsSchema, PlainTagSchema
from models import TagsModel, ItemsModel, StoresModel

bp = Blueprint(name="tags", import_name=__name__, description="Operations on tags")


@bp.route("/stores/<int:store_id>/tags")
class TagsInStoreMethods(MethodView):
    @bp.response(status_code=200, schema=PlainTagSchema(many=True))
    def get(self, store_id):
        return StoresModel.find_by_id(store_id).tags.all()

    @jwt_required()
    @bp.arguments(schema=TagSchema)
    @bp.response(status_code=201, schema=TagSchema)
    def post(self, tag_data, store_id):
        already_exists: TagsModel = StoresModel.find_by_id(store_id).tags.filter_by(name=tag_data['name']).scalar()

        if already_exists:
            abort(http_status_code=409,
                  message=tm.tag_duplicate_msg(tag_data['name'], already_exists.store.name))

        new_tag = TagsModel(**tag_data, store_id=store_id)
        new_tag.save_to_db()
        return new_tag


@bp.route("/tags/<int:tag_id>")
class TagByID(MethodView):
    @bp.response(status_code=200, schema=TagSchema)
    def get(self, tag_id):
        return TagsModel.find_by_id(tag_id)

    @jwt_required()
    @bp.response(status_code=200, description="Removes tag if no item is tagged with it")
    @bp.alt_response(status_code=400, description="Tag is still linked to items and will not be deleted")
    def delete(self, tag_id):
        tag = TagsModel.find_by_id(tag_id)

        if not tag.items:
            tag.delete_from_db()
            return tm.tag_deleted_msg(tag.name, tag.id)
        abort(http_status_code=400, message=tm.tag_still_linked_msg(tag.name))


@bp.route("/items/<int:item_id>/tags/<int:tag_id>")
class LinkUnlinkTags(MethodView):
    @jwt_required()
    @bp.response(status_code=201)
    def post(self, item_id, tag_id):
        item = ItemsModel.find_by_id(item_id)
        tag = TagsModel.find_by_id(tag_id)
        item.tags.append(tag)

        if item.store_id != tag.store_id:
            abort(http_status_code=400, message=tm.tag_item_stores_dont_match(tag.name, item.name))

        item.save_to_db()
        return tm.tag_linked_success_msg(tag.name, item.name)

    @jwt_required()
    @bp.response(status_code=200)
    def delete(self, item_id, tag_id):
        item = ItemsModel.find_by_id(item_id)
        tag = TagsModel.find_by_id(tag_id)
        item.tags.remove(tag)
        item.save_to_db()
        return tm.tag_unlinked_success_msg(tag.name, item.name)
