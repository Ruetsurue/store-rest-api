from api_lib.db import db
from models.base_model import BaseStoreApiModel


class TagsByItemsModel(BaseStoreApiModel):
    __tablename__ = "tags_by_items"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
