from flask import Blueprint, flash, render_template, redirect, url_for, jsonify
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired

from app.models.compendium import CompendiumModel

admin_compendium = Blueprint('admin_compendium', __name__, url_prefix='/admin-compendium')


class NewCompendiumForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('New Page')


@admin_compendium.route('/', methods=['GET', 'POST'])
@login_required
def all_compendium():
    form = NewCompendiumForm()
    pages = CompendiumModel.get_all()

    if form.validate_on_submit():
        if CompendiumModel.title_available(form.title.data):
            new_page = CompendiumModel(current_user.id, form.title.data).add_compendium()
            return redirect(url_for('admin_compendium.edit', compendium_id=new_page.id))
        flash('Title in use.')

    return render_template('compendium/all.html', form=form, pages=pages)


@admin_compendium.route('/<compendium_id>')
@login_required
def profile(compendium_id):
    page = CompendiumModel.get_by_id(compendium_id)

    return render_template('compendium/profile.html', page=page)


class CompendiumEditForm(FlaskForm):
    title = StringField('Title')
    content = TextAreaField('Content')
    file = FileField('File Content (will replace old content)')
    submit = SubmitField('Submit')


@admin_compendium.route('/edit/<compendium_id>', methods=['GET', 'POST'])
@login_required
def edit(compendium_id):
    page = CompendiumModel.get_by_id(compendium_id)
    form = CompendiumEditForm(
        title=page.title,
        content=page.content
    )

    if form.validate_on_submit():
        if form.title.data != page.title:
            flash(f'Page #{page.id}\'s title has been changed.')
            page.title = form.title.data

        if form.file.data:
            flash(f'Page #{page.id}\'s contents have been replaced with file contents.')

            page.content = form.file.data.read().decode('utf-8')

        elif form.content.data != page.content:
            flash(f'Page #{page.id}\'s content has been changed.')
            page.content = form.content.data

        page.add_compendium()
        return redirect(url_for('admin_compendium.edit', compendium_id=compendium_id))

    return render_template('compendium/edit.html', form=form, page=page)


@admin_compendium.route('/delete/<compendium_id>')
@login_required
def delete(compendium_id):
    CompendiumModel.get_by_id(compendium_id).delete_compendium()
    flash(f'Page #{compendium_id} has been deleted.')
    return redirect(url_for('admin_compendium.all_compendium'))


@admin_compendium.route('/json/<compendium_id>')
@login_required
def json(compendium_id):
    page = CompendiumModel.get_by_id(compendium_id)
    return jsonify(page.jsonify_dict())
