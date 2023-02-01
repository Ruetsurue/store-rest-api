from flask_smorest import abort

from api_lib.db import db
from api_lib.messages import UserMessages as um
from models.base_model import BaseStoreApiModel
from models.email_confirmation import EmailConfirmationModel


class UsersModel(BaseStoreApiModel):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(), nullable=True)
    is_privileged = db.Column(db.Boolean, default=False)
    email_confirmations = db.relationship('EmailConfirmationModel', back_populates='user', lazy='dynamic',
                                         cascade="all, delete-orphan")

    @property
    def most_recent_confirmation(self) -> EmailConfirmationModel:
        return self.email_confirmations.order_by(db.desc(EmailConfirmationModel.expires_at)).first()

    @classmethod
    def find_by_id(cls, user_id) -> "UsersModel":
        not_found_msg = um.user_not_found_by_id_msg(user_id=user_id)
        return super().find_by_id(user_id, not_found_msg)

    @classmethod
    def find_by_username(cls, username) -> "UsersModel":
        statement = db.select(cls).where(cls.username == username)
        user: cls = db.session.execute(statement).scalar()

        if not user:
            abort(http_status_code=404, message=um.user_not_found_by_name_msg(name=username))
        return user
