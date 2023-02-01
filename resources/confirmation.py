from flask import make_response, render_template, url_for, request
from flask_smorest import Blueprint, abort
from flask.views import MethodView

from api_lib.html_pages import HtmlPages as hp
from api_lib.emails import send_user_activation_email, mock_user_confirmation
from api_lib.messages import ConfirmationMessages as cm
from api_lib.schemas import EmailConfirmation
from models import EmailConfirmationModel, UsersModel


RESEND_SUCCESSFUL = ({'message': "Repeat confirmation letter has been sent"}, 201)

bp = Blueprint('confirmation', import_name=__name__, description='Operations on user signup email confirmations')


@bp.route(rule="/confirm/<string:confirmation_id>")
class ConfirmationMethods(MethodView):
    def get(self, confirmation_id: str):
        """
        Confirm user signup by id
        :param confirmation_id: id of the confirmation
        :return:
        """
        confirmation = EmailConfirmationModel.find_by_id(confirmation_id)

        if confirmation.is_confirmed:
            abort(http_status_code=400, message=cm.already_confirmed_msg())

        if confirmation.is_expired:
            abort(http_status_code=400, message=cm.confirmation_expired_msg())

        confirmation.is_confirmed = True
        confirmation.save_to_db()

        ctx = {'email': confirmation.user.email}
        headers = {"content-type": "text/html"}
        response = make_response(render_template(hp.USER_ACTIVATED_PAGE, **ctx), 200, headers)
        return response


@bp.route(rule="/confirm/user/<int:user_id>")
class ConfirmationByUserMethods(MethodView):

    @bp.response(status_code=200, schema=EmailConfirmation(many=True))
    def get(self, user_id: int) -> list[EmailConfirmationModel]:
        """
        Get all confirmations of a given user
        :param user_id: id of the user
        :return: list of confirmations
        """
        confirmations = UsersModel.find_by_id(user_id).email_confirmations.order_by(EmailConfirmationModel.expires_at)
        return confirmations

    @bp.response(status_code=201)
    def post(self, user_id: int):
        """
        Resend confirmation letter to user
        :param user_id:
        :return:
        """
        confirmation: EmailConfirmationModel = UsersModel.find_by_id(user_id).most_recent_confirmation

        if confirmation:
            if confirmation.is_confirmed:
                abort(http_status_code=400, message=cm.already_confirmed_msg())
            confirmation.force_to_expire()

        new_confirmation = EmailConfirmationModel(user_id=user_id)
        new_confirmation.save_to_db()
        # send_user_activation_email()
        activation_link = \
            f"{request.root_url[:-1]}{url_for('confirmation.ConfirmationMethods', confirmation_id=new_confirmation.id)}"
        mock_user_confirmation(activation_link=activation_link, repeat=True)

        return cm.confirmation_resend_success_msg()
