from flask import Blueprint, flash, render_template, redirect, url_for, jsonify
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

from app.models.user import UserModel
from app.models.character import CharacterModel

admin_character = Blueprint('admin_character', __name__, url_prefix='/admin-character')


class NewCharacterForm(FlaskForm):
    owner = SelectField('Owner ID', coerce=int)
    submit = SubmitField('New Character')


@admin_character.route('/', methods=['GET', 'POST'])
@login_required
def all_characters():
    form = NewCharacterForm()
    form.owner.choices = [(user.id, user.username) for user in UserModel.get_all()]
    characters = CharacterModel.get_all()

    if form.validate_on_submit():
        new_character = CharacterModel(form.owner.data).add_character()
        return redirect(url_for('admin_character.edit', character_id=new_character.id))

    return render_template('character/all.html', characters=characters, form=form)


@admin_character.route('/<character_id>')
@login_required
def profile(character_id):
    character = CharacterModel.get_by_id(character_id)

    return render_template('character/profile.html', character=character)


class CharacterEditForm(FlaskForm):
    owner = SelectField('Owner ID', coerce=int)
    name = StringField('Character Name')
    submit = SubmitField('Submit Changes')


@admin_character.route('/edit/<character_id>', methods=['GET', 'POST'])
@login_required
def edit(character_id):
    character = CharacterModel.get_by_id(character_id)
    form = CharacterEditForm(
        name=character.name
    )
    form.owner.choices = [(user.id, user.username) for user in UserModel.get_all()]
    form.owner.data = character.owner_id

    if form.validate_on_submit():
        if form.owner.data != character.owner_id:
            flash(f'Character #{character_id}\'s owner has been changed.')
            character.owner_id = form.owner.data

        if form.name.data != character.name:
            flash(f'Character #{character_id}\'s name has been changed.')
            character.name = form.name.data

        character.add_character()
        return redirect(url_for('admin_character.profile', character_id=character_id))

    return render_template('character/edit.html', character=character, form=form)


@admin_character.route('/delete/<character_id>')
@login_required
def delete(character_id):
    character = CharacterModel.get_by_id(character_id).delete_character()
    flash(f'Page #{character_id}\'s has been deleted.')
    return redirect(url_for('admin_users.edit', user_id=character.owner_id))


@admin_character.route('/json/<character_id>')
@login_required
def json(character_id):
    character = CharacterModel.get_by_id(character_id)
    return jsonify(character.jsonify_dict())
