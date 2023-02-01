from api_lib.db import db
from api_lib.messages import StoreMessages as sm
from models.base_model import BaseStoreApiModel


class StoresModel(BaseStoreApiModel):
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship("ItemsModel", back_populates="store", lazy="dynamic", cascade="all, delete")
    tags = db.relationship("TagsModel", back_populates="store", lazy="dynamic")

    @classmethod
    def find_by_id(cls, store_id) -> "StoresModel":
        not_found_msg = sm.store_not_found_by_id_msg(store_id=store_id)
        return super().find_by_id(store_id, not_found_msg)
