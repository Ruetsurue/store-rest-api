from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity
from api_lib.tokens import revoke_token
from schemas import UserSchema
from db import db
from models import UsersModel
from passlib.hash import pbkdf2_sha256

blueprint = Blueprint(name="users", import_name=__name__, description="Operations on users")


@blueprint.route(rule="/signup")
class SignupMethods(MethodView):
    @blueprint.arguments(schema=UserSchema)
    @blueprint.response(status_code=201)
    def post(self, userdata):
        statement = db.select(UsersModel).where(UsersModel.username == userdata['username'])
        user_exists = db.session.execute(statement).scalars().all()

        if user_exists:
            abort(http_status_code=409, message="User already exists")

        new_user = UsersModel(username=userdata['username'],
                              password=pbkdf2_sha256.hash(userdata['password']),
                              is_privileged=userdata.get('is_privileged'))
        db.session.add(new_user)
        db.session.commit()

        return {"message": f"User {userdata['username']} created"}


@blueprint.route(rule="/login")
class LoginMethods(MethodView):
    @blueprint.arguments(schema=UserSchema)
    def post(self, userdata):
        statement = db.select(UsersModel).where(UsersModel.username == userdata['username'])
        user_record: UsersModel = db.session.execute(statement).scalar()

        if not user_record:
            abort(http_status_code=404, message="No such user")

        if pbkdf2_sha256.verify(userdata['password'], user_record.password):
            access_token = create_access_token(identity=user_record.id, fresh=True)
            refresh_token = create_refresh_token(identity=user_record.id)
            return {"access_token": access_token, "refresh_token": refresh_token}

        abort(http_status_code=401, message="Failed to authorize. Incorrect password")


@blueprint.route(rule="/refresh")
class RefreshMethods(MethodView):
    @jwt_required(refresh=True)
    def get(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}


@blueprint.route(rule="/logout")
class LogoutMethods(MethodView):
    @jwt_required()
    def get(self):
        jwt = get_jwt()
        jti = jwt.get('jti')
        revoke_token(token_id=jti)

        return {"message": "Logged out"}


@blueprint.route(rule="/users/<int:user_id>")
class UserMethods(MethodView):
    @blueprint.response(status_code=200, schema=UserSchema)
    def get(self, user_id):
        user = db.get_or_404(entity=UsersModel, ident=user_id)
        return user

    @jwt_required()
    def delete(self, user_id):
        user = db.get_or_404(entity=UsersModel, ident=user_id)
        username = user.username
        db.session.delete(user)
        db.session.commit()

        return {"message": f"Deleted: User_id: {user_id}, username: {username}"}
