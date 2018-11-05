from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/<int:id>/updateuser', methods=('GET', 'POST'))
@login_required
def updateuser(id):
    user = get_user(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE qid = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('question.index'))

    return render_template('user/updateuser.html', user=user)

def get_user(id, check_author=True):
    post = get_db().execute(
        'SELECT qid, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE qid = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/username',  methods=('GET','POST'))
def username(id):
    db = get_db()
    posts=db.execute('SELECT * FROM post WHERE qid = ?', (id,)).fetchone()
    ans=db.execute('SELECT * FROM answer WHERE qid = ?', (id,)).fetchall()
    ans_len=len(ans)
    return render_template('user/username.html',posts=posts,ans=ans,ans_len=ans_len)