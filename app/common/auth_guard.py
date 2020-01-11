from flask_jwt_extended import get_jwt_identity

from app import login
from app.common.error_handling import NotFoundError, NotOwnerError, NotAuthorizedError
from app.models.user import UserModel
from app.models.character import CharacterModel


@login.user_loader
def load_user(user_id):
    return UserModel.get_by_id(user_id)


login.login_view = 'admin_main.login'


def get_character_patch(char_id):
    character = CharacterModel.get_by_id(char_id)
    if not character:
        raise NotFoundError()
    elif character.owner_id != get_jwt_identity():
        raise NotOwnerError()
    else:
        return character


def get_character_view(char_id):
    character = CharacterModel.get_by_id(char_id)

    if not character:
        raise NotFoundError()
    elif not (character.owner_id == get_jwt_identity() or get_jwt_identity() in character.viewers):
        raise NotAuthorizedError()
    else:
        return character
