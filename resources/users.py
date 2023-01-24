from flask import render_template, make_response, url_for, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity
from api_lib.tokens import revoke_token, confirm_password, hash_password
from api_lib.schemas import UserSchema
from api_lib.db import db
from api_lib.msg_templates import EntityErrorTemplates as eet, AuthErrorTemplates as aet, AuthInfoTemplates as ait, \
    EntityInfoTemplates as eit
from api_lib.emails import send_user_activation_email
from models import UsersModel

ENTITY_TYPE = 'user'
USER_ACTIVATED_PAGE = 'user_activated.html'
USER_CREATED_PAGE = 'user_created.html'

blueprint = Blueprint(name="users", import_name=__name__, description="Operations on users")


@blueprint.route(rule="/signup")
class SignupMethods(MethodView):
    @blueprint.arguments(schema=UserSchema)
    @blueprint.response(status_code=201)
    def post(self, userdata):
        statement = db.select(UsersModel).where(UsersModel.username == userdata['username'])
        user_already_exists: UsersModel = db.session.execute(statement).scalar()

        if user_already_exists:
            abort(http_status_code=409, message=eet.entity_duplicate_msg(ENTITY_TYPE, user_already_exists.username))

        userdata['password'] = hash_password(userdata['password'])
        new_user = UsersModel(**userdata)
        db.session.add(new_user)
        db.session.commit()

        activation_link = f"{request.root_url[:-1]}{url_for('users.ActivateMethods', user_id=new_user.id)}"
        # email_to = new_user.email
        # send_user_activation_email(activation_link=activation_link, email_to=email_to)

        # return {"message": f"Account created successfully. Please check your email {email_to} for activaiton link"}, 201
        ctx = {'activation_link': activation_link}
        headers = {"content-type": "text/html"}
        response = make_response(render_template(USER_CREATED_PAGE, **ctx), 200, headers)

        return response


@blueprint.route(rule="/activate/<int:user_id>")
class ActivateMethods(MethodView):
    def get(self, user_id):
        user: UsersModel = db.get_or_404(entity=UsersModel, ident=user_id)
        user.is_activated = True
        db.session.add(user)
        db.session.commit()
        ctx = {'email': user.email}
        headers = {"content-type": "text/html"}
        response = make_response(render_template(USER_ACTIVATED_PAGE, **ctx), 200, headers)
        return response


@blueprint.route(rule="/login")
class LoginMethods(MethodView):
    @blueprint.arguments(schema=UserSchema(partial=('email',)))
    def post(self, userdata):
        statement = db.select(UsersModel).where(UsersModel.username == userdata['username'])
        user: UsersModel = db.session.execute(statement).scalar()

        if not user:
            abort(http_status_code=404, message=eet.entity_missing_by_name_msg(ENTITY_TYPE, userdata['username']))

        if confirm_password(attempted_password=userdata['password'], db_hash_password=user.password):
            if user.is_activated:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(identity=user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}
            abort(http_status_code=403,
                  message=aet.user_not_activated_msg(ENTITY_TYPE, userdata['username'],
                                                     email=user.email))

        abort(http_status_code=401, message=aet.incorrect_password_msg(ENTITY_TYPE, userdata['username']))


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

        return ait.logout_msg(jsonify=True)


@blueprint.route(rule="/users/<int:user_id>")
class UserMethods(MethodView):
    @blueprint.response(status_code=200, schema=UserSchema)
    def get(self, user_id):
        user = db.get_or_404(entity=UsersModel, ident=user_id)
        return user

    @jwt_required()
    def delete(self, user_id):
        user: UsersModel = db.get_or_404(entity=UsersModel, ident=user_id)
        db.session.delete(user)
        db.session.commit()

        return eit.entity_deleted_msg(ENTITY_TYPE, user.username, user_id, jsonify=True)
