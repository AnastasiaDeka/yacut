from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import URLForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if form.validate_on_submit():
        original = form.original_link.data
        custom_id = form.custom_id.data

        if custom_id:
            if URLMap.query.filter_by(short=custom_id).first():
                flash(
                    'Предложенный вариант короткой ссылки уже существует.',
                    'error'
                )
                return render_template('yacut.html', form=form)
            short = custom_id
        else:
            short = get_unique_short_id()

        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        short_url = url_for('follow_link', short=short, _external=True)
        flash(short_url, 'short_link')
        return render_template('yacut.html', form=form)

    return render_template('yacut.html', form=form)


@app.route('/<string:short>')
def follow_link(short):
    url_map = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url_map.original)
