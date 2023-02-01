from flask_babel import _


# _ stands for babel.gettext()
class UserMessages:
    @classmethod
    def user_duplicate_msg(cls, name):
        return _('User by name %(name)s already exists', name=name)

    @classmethod
    def user_not_found_by_name_msg(cls, name):
        return _('User by name %(name)s not found', name=name)

    @classmethod
    def user_not_found_by_id_msg(cls, user_id):
        return _('User by id %(user_id)s not found', user_id=user_id)

    @classmethod
    def user_deleted_msg(cls, username, user_id):
        return _('User %(username)s (id %(user_id)s) successfully deleted', username=username, user_id=user_id)

    @classmethod
    def user_not_confirmed_msg(cls, name, email):
        return _('User %(name)s not activated. Check email %(email)s for activation link', name=name, email=email)

    @classmethod
    def user_incorrect_password_msg(cls, name):
        return _("Failed to authorize. Incorrect password for user %(name)s", name=name)

    @classmethod
    def user_logout_msg(cls):
        return _("Logged out")


class StoreMessages:
    @classmethod
    def store_duplicate_msg(cls, name):
        return _('Store by name %(name)s already exists', name=name)

    @classmethod
    def store_not_found_by_id_msg(cls, store_id):
        return _('Store by id %(store_id)s not found', store_id=store_id)

    @classmethod
    def store_deleted_msg(cls, name, store_id):
        return _('Store %(name)s (id %(store_id)s) successfully deleted', name=name, store_id=store_id)


class ItemMessages:
    @classmethod
    def item_duplicate_msg(cls, name):
        return _('Item by name %(name)s already exists', name=name)

    @classmethod
    def item_not_found_by_id_msg(cls, item_id):
        return _('Item by id %(item_id)s not found', item_id=item_id)

    @classmethod
    def item_deleted_msg(cls, name, item_id):
        return _('Item %(name)s (id %(item_id)s) successfully deleted', name=name, item_id=item_id)
    

class TagMessages:
    @classmethod
    def tag_duplicate_msg(cls, tag_name, store_name):
        return _('Tag %(tag_name)s already exists in store %(store_name)s', tag_name=tag_name, store_name=store_name)

    @classmethod
    def tag_not_found_by_id_msg(cls, tag_id):
        return _('Tag by id %(tag_id)s not found', tag_id=tag_id)

    @classmethod
    def tag_deleted_msg(cls, name, tag_id):
        return _('Tag %(name)s (id %(tag_id)s) successfully deleted', name=name, tag_id=tag_id)

    @classmethod
    def tag_linked_success_msg(cls, tag_name, item_name):
        return _("Tag %(tag_name)s successfully linked to item %(item_name)s",
                 tag_name=tag_name, item_name=item_name)

    @classmethod
    def tag_unlinked_success_msg(cls, tag_name, item_name):
        return _("Tag %(tag_name)s successfully unlinked from item %(item_name)s",
                 tag_name=tag_name, item_name=item_name)

    @classmethod
    def tag_still_linked_msg(cls, name):
        return _("Tag %(name)s is still linked to items and will not be deleted", name=name)

    @classmethod
    def tag_item_stores_dont_match(cls, tag_name, item_name):
        return _("Tag %(tag_name)s and item %(item_name)s belong to different stores and cannot be linked",
                 tag_name=tag_name, item_name=item_name)
    
    
class ConfirmationMessages:
    @classmethod
    def confirmation_not_found_by_id_msg(cls, confirmation_id):
        return _('Confirmation by id %(confirmation_id)s not found', confirmation_id=confirmation_id)

    @classmethod
    def already_confirmed_msg(cls):
        return _('This confirmation is already confirmed')

    @classmethod
    def confirmation_expired_msg(cls):
        return _('This confirmation has expired')

    @classmethod
    def confirmation_resend_success_msg(cls):
        return _('Repeat confirmation letter has been sent')


class DBMessages:
    @classmethod
    def insertion_err(cls, err):
        return _('Error inserting into db. Error:\n %(err)s', err=str(err))

    @classmethod
    def deletion_err(cls, err):
        return _('Error deleting from db. Error:\n %(err)s', err=str(err))

    @classmethod
    def integrity_err(cls, entity_name, err):
        return _('Object with name %(entity_name)s already exists. Error:\n %(err)s',
                 entity_name=entity_name, err=str(err))


class AuthMessages:
    @classmethod
    def token_revoked_msg(cls):
        return _('This token has been revoked')

    @classmethod
    def requires_fresh_msg(cls):
        return _('This action requires a fresh token. Re-login')
