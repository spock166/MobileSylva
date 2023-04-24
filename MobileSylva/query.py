from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from MobileSylva.auth import login_required
from MobileSylva.db import get_db

bp = Blueprint('query', __name__)

@bp.route('/')
def index():
    db = get_db()
    queries = db.execute(
        'SELECT p.id, content, answered, answer, created, author_id, username'
        ' FROM query p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('query/index.html', queries=queries)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        content = request.form['content']
        error = None

        if not content:
            error = 'Empty queries make Sylva sad.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO query (content, author_id)'
                ' VALUES (?, ?)',
                (content, g.user['id'])
            )
            db.commit()
            return redirect(url_for('query.index'))

    return render_template('query/create.html')