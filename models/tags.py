from api_lib.db import db
from api_lib.messages import TagMessages as tm
from models.base_model import BaseStoreApiModel


class TagsModel(BaseStoreApiModel):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    store = db.relationship("StoresModel", back_populates="tags")
    items = db.relationship("ItemsModel", back_populates="tags", secondary="tags_by_items")

    @classmethod
    def find_by_id(cls, tag_id) -> "TagsModel":
        not_found_msg = tm.tag_not_found_by_id_msg(tag_id=tag_id)
        return super().find_by_id(tag_id, not_found_msg)
