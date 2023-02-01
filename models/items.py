from api_lib.db import db
from api_lib.messages import ItemMessages as im
from models.base_model import BaseStoreApiModel


class ItemsModel(BaseStoreApiModel):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2))
    description = db.Column(db.String())
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    store = db.relationship("StoresModel", back_populates="items")
    tags = db.relationship("TagsModel", back_populates="items", secondary="tags_by_items")

    @classmethod
    def find_by_id(cls, item_id) -> "ItemsModel":
        not_found_msg = im.item_not_found_by_id_msg(item_id=item_id)
        return super().find_by_id(item_id, not_found_msg)
