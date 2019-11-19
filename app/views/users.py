from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from app.models.user import UserModel

admin_users = Blueprint('admin_users', __name__, url_prefix='/admin-users')


class NewUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('New User')


@admin_users.route('/', methods=['GET', 'POST'])
@login_required
def all_users():
    form = NewUserForm()
    users = UserModel.get_all()

    if form.validate_on_submit():
        user = UserModel(form.username.data, 'temppassword').add_user()
        return redirect(url_for('admin_users.edit', user_id=user.id))

    return render_template('users/all.html', users=users, form=form)


@admin_users.route('/<user_id>')
@login_required
def profile(user_id):
    user = UserModel.get_by_id(user_id)

    return render_template('users/profile.html', user=user)


class UserEditForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Change User Data')


@admin_users.route('/edit/<user_id>', methods=['GET', 'POST'])
@login_required
def edit(user_id):
    user = UserModel.get_by_id(user_id)
    form = UserEditForm(
        username=user.username
    )

    if form.validate_on_submit():
        if form.username.data != user.username:
            flash(f'User #{user.id}\'s name has been changed.')
            user.change_username(form.username.data)

        if form.password.data != "":
            flash(f'User #{user.id}\'s password has been changed.')
            user.change_password(form.password.data)

        return redirect(url_for('admin_users.profile', user_id=user_id))

    return render_template('users/edit.html', user=user, form=form)


@admin_users.route('/delete/<user_id>')
@login_required
def delete(user_id):
    user = UserModel.get_by_id(user_id)
    if user.type != 'super':
        user.delete_user()
        flash(f'User #{user_id} has been deleted.')
    else:
        flash(f'User #{user_id} can\'t be deleted')

    return redirect(url_for('admin_users.all_users'))


@admin_users.route('/new/<username>')
@login_required
def new(username):
    user = UserModel(username, 'temppassword')

    return redirect(url_for('admin_users.edit', user_id=user.id))
