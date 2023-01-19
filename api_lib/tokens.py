from flask_jwt_extended import JWTManager
from flask import Flask, jsonify
from api_lib.db import db
from models import UsersModel

# dummy mocking the token db
BLOCKLIST = set()
# dummy mocking the token db


def revoke_token(token_id):
    BLOCKLIST.add(token_id)


def create_jwt_manager(app: Flask):
    jwt = JWTManager(app=app)

    @jwt.token_in_blocklist_loader
    def is_token_revoked(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def on_token_revoked(jwt_header, jwt_payload):
        return jsonify(
            {"description": "This token has been revoked",
             "error": "token_revoked"}
        ), 401

    @jwt.additional_claims_loader
    def add_additional_claims(identity):
        statement = db.select(UsersModel.is_privileged).where(UsersModel.id == identity)
        is_privileged = db.session.execute(statement).scalar()
        return {"is_privileged": is_privileged}

    @jwt.needs_fresh_token_loader
    def on_needs_fresh_token(jwt_header, jwt_payload):
        return jsonify(
            {"description": "This action requires a fresh token",
             "error": "fresh_token_required"}
        ), 401
