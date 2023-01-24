from flask import jsonify, Response
from typing import Union


class MessageTemplates:
    @classmethod
    # for use exclusively when returning JSON unwrapped into a Response obj
    def _jsonify_message(cls, message: str):
        return jsonify({"message": message})

    @classmethod
    def _enrich(cls, message: str, *args, **kwargs) -> Union[str, Response]:
        if kwargs.get('jsonify'):
            message = MessageTemplates._jsonify_message(message=message)
        return message


class ErrorTemplates(MessageTemplates):
    @classmethod
    def _add_err(cls, message: Union[str, Response], err: Exception) -> str:
        return '\n'.join(message, str(err))

    @classmethod
    def _enrich(cls, message: str, *args, **kwargs) -> Union[str, Response]:
        if kwargs.get('err'):
            message = ErrorTemplates._add_err(message=message, err=kwargs['err'])
        return super()._enrich(message, *args, **kwargs)


class EntityErrorTemplates(ErrorTemplates):
    @classmethod
    def entity_missing_msg(cls, entity_type='', entity_name='', entity_id='', jsonify=False, err=None):
        message = f"{entity_type.capitalize()} {entity_name} (id={entity_id}) not found"
        return super()._enrich(message, jsonify=jsonify, err=err)

    @classmethod
    def entity_missing_by_name_msg(cls, entity_type='', entity_name='', entity_id='', jsonify=False, err=None):
        message = f"{entity_type.capitalize()} by name {entity_name} not found"
        return super()._enrich(message, jsonify=jsonify, err=err)

    @classmethod
    def entity_duplicate_msg(cls, entity_type='', entity_name='', entity_id='', jsonify=False, err=None):
        message = f"{entity_type.capitalize()} with name {entity_name} already exists"
        return super()._enrich(message, jsonify=jsonify, err=err)


class DBErrorTemplates(ErrorTemplates):
    @classmethod
    def db_insertion_err_msg(cls, entity_type='', entity_name='', entity_id='', jsonify=False, err=None):
        message = f"Error inserting into db:"
        return super()._enrich(message, jsonify=jsonify, err=err)


class AuthErrorTemplates(ErrorTemplates):
    @classmethod
    def incorrect_password_msg(cls, entity_type='', entity_name='', entity_id='', jsonify=False, err=None):
        message = f"Failed to authorize. Incorrect password for {entity_type} {entity_name}"
        return super()._enrich(message, jsonify=jsonify, err=err)

    @classmethod
    def user_not_activated_msg(cls, entity_type='', entity_name='', entity_id='', jsonify=False, err=None, email=''):
        message = f"{entity_type.capitalize()} {entity_name} not activated. Check email {email} for activation link"
        return super()._enrich(message, jsonify=jsonify, err=err)


class InfoTemplates(MessageTemplates):
    pass


class EntityInfoTemplates(InfoTemplates):
    @classmethod
    def entity_created_msg(cls, entity_type='', entity_name='', entity_id='', jsonify=False):
        message = f"{entity_type.capitalize()} {entity_name} created"
        return super()._enrich(message, jsonify=jsonify)

    @classmethod
    def entity_deleted_msg(cls, entity_type='', entity_name='', entity_id='', jsonify=False):
        message = f"{entity_type.capitalize()} {entity_name} (id={entity_id}) deleted"
        return super()._enrich(message, jsonify=jsonify)


class AuthInfoTemplates(InfoTemplates):
    @classmethod
    def user_activated_msg(cls, entity_type='', entity_name='', entity_id='', jsonify=False):
        message = f"Succesfully activated {entity_type} {entity_name}"
        return super()._enrich(message, jsonify=jsonify)

    @classmethod
    def logout_msg(cls, jsonify=False):
        message = f"Logged out"
        return super()._enrich(message, jsonify=jsonify)
