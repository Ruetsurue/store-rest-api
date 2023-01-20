from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from api_lib.schemas import StoreSchema
from api_lib.db import db
from api_lib.message_templates import EntityErrorTemplates as eet, EntityInfoTemplates as eit, DBErrorTemplates as det
from models import StoresModel

ENTITY_TYPE = 'store'
blueprint = Blueprint(name="stores", import_name=__name__, description="Operations on stores")


@blueprint.route(rule="/stores")
class StoreMethods(MethodView):
    @blueprint.response(status_code=200, schema=StoreSchema(many=True))
    def get(self):
        statement = db.select(StoresModel)
        return db.session.execute(statement).scalars().all()

    @jwt_required(fresh=False)
    @blueprint.arguments(schema=StoreSchema)
    @blueprint.response(status_code=201, schema=StoreSchema)
    def post(self, store_data):
        new_store = StoresModel(**store_data)
        try:
            db.session.add(new_store)
            db.session.commit()
        except IntegrityError as err:
            abort(http_status_code=400, message=eet.entity_duplicate_msg(ENTITY_TYPE, new_store.name, err=err))
        except SQLAlchemyError as err:
            abort(http_status_code=500, message=det.db_insertion_err_msg(ENTITY_TYPE, new_store.name, err=err))
        return new_store


@blueprint.route(rule="/stores/<int:store_id>")
class StoreByIDMethods(MethodView):
    @blueprint.response(status_code=200, schema=StoreSchema)
    def get(self, store_id):
        desc = eet.entity_missing_msg(entity_type=ENTITY_TYPE, entity_id=store_id)
        return db.get_or_404(entity=StoresModel,
                             ident=store_id,
                             description=desc)

    @jwt_required(fresh=True)
    def delete(self, store_id):
        store: StoresModel = db.get_or_404(entity=StoresModel, ident=store_id)
        db.session.delete(store)
        db.session.commit()

        return eit.entity_deleted_msg(entity_type=ENTITY_TYPE,
                                      entity_name=store.name,
                                      entity_id=store.id,
                                      jsonify=True)
