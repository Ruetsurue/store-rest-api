import os
import requests
from flask import render_template, make_response
from api_lib.html_pages import HtmlPages as hp

APP_TITLE = 'Store REST API'


def mock_user_confirmation(activation_link: str, repeat=False):
    ctx = {'activation_link': activation_link}
    headers = {"content-type": "text/html"}

    if repeat:
        page = hp.USER_REPEAT_ACTIVATION_PAGE
    else:
        page = hp.USER_CREATED_PAGE

    response = make_response(render_template(page, **ctx), 200, headers)
    return response


def send_user_activation_email(activation_link: str, email_to=None):
    email_api_provider = os.getenv('MAILJET_DOMAIN')
    auth = (os.getenv('MAILJET_API_KEY_PUBLIC'), os.getenv('MAILJET_API_KEY_PRIVATE'))
    email_to = email_to or os.getenv('MOCK_USER_EMAIL')
    payload = {
        "from": f"{ APP_TITLE } <{ os.getenv('MAILJET_EMAIL') }>",
        "to": f"{email_to}",
        "subject": "User activation at Store REST API",
        "text": f"Thanks for signing up! Follow this link to activate your account: {activation_link}"
    }

    payload = {"messages": [payload]}
    return requests.post(url=email_api_provider, data=payload, auth=auth)
