from flask_smorest import abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from api_lib.db import db
from api_lib.messages import DBMessages as dbm


class BaseStoreApiModel(db.Model):
    __abstract__ = True

    @classmethod
    def find_by_id(cls, entity_id, not_found_msg):
        entity: cls = db.session.get(entity=cls, ident=entity_id)

        if not entity:
            abort(http_status_code=404, message=not_found_msg)

        return entity

    @classmethod
    def get_all(cls):
        statement = db.select(cls)
        result = db.session.execute(statement).scalars().all()
        return result

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as err:
            abort(http_status_code=500, message=dbm.integrity_err(self.name, err))
        except SQLAlchemyError as err:
            abort(http_status_code=500, message=dbm.insertion_err(err))

    def delete_from_db(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as err:
            abort(http_status_code=500, message=dbm.deletion_err(err))
