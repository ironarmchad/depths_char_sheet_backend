from flask_jwt_extended import get_jwt_identity

from app.common.error_handling import NotFoundError, NotOwnerError
from app.models.character import CharacterModel


def get_character(char_id):
    character = CharacterModel.get_by_id(char_id)
    if not character:
        raise NotFoundError()
    elif character.owner != get_jwt_identity():
        raise NotOwnerError()
    else:
        return character
