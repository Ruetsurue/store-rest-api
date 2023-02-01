import time

from api_lib.db import db
from api_lib.messages import ConfirmationMessages as cm
from models.base_model import BaseStoreApiModel
from uuid import uuid4


EXPIRES_IN_SECONDS = 1800
NOT_FOUND = ({'message': "Confirmation not found"}, 404)


class EmailConfirmationModel(BaseStoreApiModel):
    __tablename__ = "email_confirmations"
    id = db.Column(db.String(80), primary_key=True)
    expires_at = db.Column(db.Integer, nullable=False)
    is_confirmed = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UsersModel', back_populates='email_confirmations')

    def __init__(self, user_id: int, **kwargs) -> "EmailConfirmationModel":
        super().__init__(**kwargs)
        self.id = uuid4().hex
        self.expires_at = int(time.time()) + EXPIRES_IN_SECONDS
        self.is_confirmed = False
        self.user_id = user_id

    @classmethod
    def find_by_id(cls, confirmation_id: str) -> "EmailConfirmationModel":
        not_found_msg = cm.confirmation_not_found_by_id_msg(confirmation_id)
        return super().find_by_id(confirmation_id, not_found_msg)

    @property
    def is_expired(self) -> bool:
        return time.time() > self.expires_at

    def force_to_expire(self):
        if not self.is_expired:
            self.expires_at = time.time()
            self.save_to_db()
