from flask import url_for, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity

from api_lib.messages import UserMessages as um
from api_lib.tokens import revoke_token, confirm_password, hash_password
from api_lib.schemas import UserSchema
from api_lib.html_pages import HtmlPages as hp
from api_lib.emails import send_user_activation_email, mock_user_confirmation
from models import UsersModel, EmailConfirmationModel

bp = Blueprint(name="users", import_name=__name__, description="Operations on users")


@bp.route(rule="/signup")
class SignupMethods(MethodView):
    @bp.arguments(schema=UserSchema)
    @bp.response(status_code=201)
    def post(self, userdata):
        user_already_exists = UsersModel.find_by_username(userdata['username'])

        if user_already_exists:
            abort(http_status_code=409, message=um.user_duplicate_msg(name=userdata['username']))

        userdata['password'] = hash_password(userdata['password'])
        new_user = UsersModel(**userdata)
        new_user.save_to_db()

        user_confirmation = EmailConfirmationModel(user_id=new_user.id)
        user_confirmation.save_to_db()

        activation_link = \
            f"{request.root_url[:-1]}{url_for('confirmation.ConfirmationMethods', confirmation_id=user_confirmation.id)}"
        # email_to = new_user.email
        # send_user_activation_email(activation_link=activation_link, email_to=email_to)
        response = mock_user_confirmation(activation_link=activation_link)

        return response


@bp.route(rule="/login")
class LoginMethods(MethodView):
    @bp.arguments(schema=UserSchema(partial=('email',)))
    def post(self, userdata):
        user = UsersModel.find_by_username(userdata['username'])

        if confirm_password(attempted_password=userdata['password'], db_hash_password=user.password):
            if user.most_recent_confirmation.is_confirmed:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(identity=user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}

            abort(http_status_code=403, message=um.user_not_confirmed_msg(name=userdata['username'], email=user.email))

        abort(http_status_code=401, message=um.user_incorrect_password_msg(name=userdata['username']))


@bp.route(rule="/refresh")
class RefreshMethods(MethodView):
    @jwt_required(refresh=True)
    def get(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}


@bp.route(rule="/logout")
class LogoutMethods(MethodView):
    @jwt_required()
    def get(self):
        jwt = get_jwt()
        jti = jwt.get('jti')
        revoke_token(token_id=jti)

        return um.user_logout_msg()


@bp.route(rule="/users/<int:user_id>")
class UserMethods(MethodView):
    @bp.response(status_code=200, schema=UserSchema)
    def get(self, user_id):
        return UsersModel.find_by_id(user_id)

    @jwt_required()
    def delete(self, user_id):
        user = UsersModel.find_by_id(user_id)
        user.delete_from_db()

        return um.user_deleted_msg(user.username, user_id)
