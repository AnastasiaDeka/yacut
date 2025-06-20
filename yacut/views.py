from flask import flash, redirect, render_template

from . import app
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()

    if not form.validate_on_submit():
        return render_template('yacut.html', form=form)

    original = form.original_link.data
    custom_id = form.custom_id.data

    try:
        url_map = URLMap.create(original, custom_id)
    except ValueError as error:
        flash(str(error), 'error')
        return render_template('yacut.html', form=form)

    short_url = url_map.to_dict()['short_link']
    flash(short_url, 'short_link')
    return render_template('yacut.html', form=form)


@app.route('/<string:short>')
def follow_link(short):
    url_map = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url_map.original)
