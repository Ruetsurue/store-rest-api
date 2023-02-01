from flask_jwt_extended import JWTManager
from flask import Flask, jsonify
from passlib.hash import pbkdf2_sha256

from api_lib.messages import AuthMessages as am
from models import UsersModel

# dummy mocking the token db
BLOCKLIST = set()
# dummy mocking the token db


def hash_password(password):
    return pbkdf2_sha256.hash(password)


def confirm_password(attempted_password, db_hash_password):
    return pbkdf2_sha256.verify(attempted_password, db_hash_password)


def revoke_token(token_id):
    BLOCKLIST.add(token_id)


def create_jwt_manager(app: Flask):
    jwt = JWTManager(app=app)
    configure_jwt_loaders(jwt=jwt)


def configure_jwt_loaders(jwt: JWTManager):
    @jwt.token_in_blocklist_loader
    def is_token_revoked(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def on_token_revoked(jwt_header, jwt_payload):
        return jsonify(
            {"description": am.token_revoked_msg(),
             "error": "token_revoked"}
        ), 401

    @jwt.additional_claims_loader
    def add_additional_claims(identity):
        is_privileged = UsersModel.find_by_id(identity).is_privileged
        return {"is_privileged": is_privileged}

    @jwt.needs_fresh_token_loader
    def on_needs_fresh_token(jwt_header, jwt_payload):
        return jsonify(
            {"description": am.requires_fresh_msg(),
             "error": "fresh_token_required"}
        ), 401
