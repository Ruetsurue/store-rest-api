from flask import jsonify, Response
from typing import Union


class MessageTemplates:
    @staticmethod
    def _jsonify_message(message: str) -> Response:
        return jsonify({"message": message})

    @staticmethod
    def _enrich(message: str, *args, **kwargs) -> Union[str, Response]:
        if kwargs.get('jsonify'):
            message = MessageTemplates._jsonify_message(message=message)
        return message


class ErrorTemplates(MessageTemplates):
    @staticmethod
    def _add_err(message: Union[str, Response], err: Exception) -> str:
        return '\n'.join(message, str(err))

    @staticmethod
    def _enrich(message: str, *args, **kwargs) -> Union[str, Response]:
        if kwargs.get('err'):
            message = ErrorTemplates._add_err(message=message, err=kwargs['err'])
        return super()._enrich(message, *args, **kwargs)


class EntityErrorTemplates(ErrorTemplates):
    @staticmethod
    def entity_missing_msg(entity_type='', entity_name='', entity_id='', jsonify=False, err=None):
        message = f"{entity_type.capitalize()} {entity_name} (id={entity_id}) not found"
        return super()._enrich(message, jsonify=jsonify, err=err)

    @staticmethod
    def entity_missing_by_name_msg(entity_type='', entity_name='', entity_id='', jsonify=False, err=None):
        message = f"{entity_type.capitalize()} by name {entity_name} not found"
        return super()._enrich(message, jsonify=jsonify, err=err)

    @staticmethod
    def entity_duplicate_msg(entity_type='', entity_name='', entity_id='', jsonify=False, err=None):
        message = f"{entity_type.capitalize()} with name {entity_name} already exists"
        return super()._enrich(message, jsonify=jsonify, err=err)


class DBErrorTemplates(ErrorTemplates):
    @staticmethod
    def db_insertion_err_msg(entity_type='', entity_name='', entity_id='', jsonify=False, err=None):
        message = f"Error inserting into db:"
        return super()._enrich(message, jsonify=jsonify, err=err)


class AuthErrorTemplates(ErrorTemplates):
    @staticmethod
    def incorrect_password_msg(entity_type='', entity_name='', entity_id='', jsonify=False, err=None):
        message = f"Failed to authorize. Incorrect password for {entity_type} {entity_name}"
        return super()._enrich(message, jsonify=jsonify, err=err)


class InfoTemplates(MessageTemplates):
    pass


class EntityInfoTemplates(InfoTemplates):
    @staticmethod
    def entity_created_msg(entity_type='', entity_name='', entity_id='', jsonify=False):
        message = f"{entity_type.capitalize()} {entity_name} created"
        return super()._enrich(message, jsonify=jsonify)

    @staticmethod
    def entity_deleted_msg(entity_type='', entity_name='', entity_id='', jsonify=False):
        message = f"{entity_type.capitalize()} {entity_name} (id={entity_id}) deleted"
        return super()._enrich(message, jsonify=jsonify)


class AuthInfoTemplates(ErrorTemplates):
    @staticmethod
    def incorrect_password_msg(entity_type='', entity_name='', entity_id='', jsonify=False):
        message = f"Failed to authorize. Incorrect password for {entity_type} {entity_name}"
        return super()._enrich(message, jsonify=jsonify)

    @staticmethod
    def logout_msg(jsonify=False):
        message = f"Logged out"
        return super()._enrich(message, jsonify=jsonify)
