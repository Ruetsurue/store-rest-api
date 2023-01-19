from api_lib.db import db


class StoresModel(db.Model):
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship("ItemsModel", back_populates="store", lazy="dynamic", cascade="all, delete")
    tags = db.relationship("TagsModel", back_populates="store", lazy="dynamic")
