from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from app.models.user import UserModel

admin_main = Blueprint('admin_main', __name__, url_prefix='/admin')


@admin_main.route('/')
@login_required
def home():
    return render_template('main/home.html')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


@admin_main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = UserModel.get_by_username(form.username.data)
        if user is None or user.type != 'super' or user.check_password(form.password.data):
            flash('Incorrect Username or Password')
            return redirect(url_for('main.login'))
        flash(f'User {user.username} has been logged in.')
        login_user(user)
        return redirect(url_for('main.home'))
    return render_template('main/login.html', form=form)


@admin_main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))
