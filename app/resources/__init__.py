from flask_jwt_extended import get_jwt_identity

from app.models.character import CharacterModel


class Error(Exception):
    def __init__(self, message):
        self.message = message


class NotFoundError(Error):
    def __init__(self):
        super().__init__('Ability could not be found')


class NotOwnerError(Error):
    def __init__(self):
        super().__init__('Cannot access another players character.')


def get_character(char_id):
    character = CharacterModel.get_by_id(char_id)
    if not character:
        raise NotFoundError()
    elif character.owner != get_jwt_identity():
        raise NotOwnerError()
    else:
        return character
