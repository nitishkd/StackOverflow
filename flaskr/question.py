from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('question', __name__)
@bp.route('/')
def index():
    db=get_db()
    posts = db.execute(
        'SELECT qid, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('question/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
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
                'INSERT INTO post (author_id,title,body,tag)'
                ' VALUES (?, ?, ?, ?)',
                ( g.user['id'],title, body,"some_tag")
            )
            db.commit()
            return redirect(url_for('question.index'))

    return render_template('question/create.html')

def get_question(id, check_author=True):
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

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_question(id)

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

    return render_template('question/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_question(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE qid = ?', (id,))
    db.commit()
    return redirect(url_for('question.index'))


@bp.route('/<int:id>/que',  methods=('GET','POST'))
def que(id):
    db = get_db()
    posts=db.execute('SELECT * FROM post WHERE qid = ?', (id,)).fetchone()
    ans=db.execute('SELECT * FROM answer WHERE qid = ?', (id,)).fetchall()
    ans_len=len(ans)
    return render_template('question/que.html',posts=posts,ans=ans,ans_len=ans_len)

@bp.route('/<int:id>/createanswer', methods=('GET', 'POST'))
@login_required
def createanswer(id):
    if request.method == 'POST':
        body = request.form['body']
        db = get_db()
        db.execute(
            'INSERT INTO answer (qid,author_id,body)'
            ' VALUES (?, ?, ?)',
            (id, g.user['id'], body)
        )
        db.commit()
        return redirect(url_for("question.que", id=id))

    return render_template('question/createanswer.html')

def get_answer(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, qid, body, created, author_id, username'
        ' FROM answer p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/updateanswer', methods=('GET', 'POST'))
@login_required
def updateanswer(id):
    post = get_answer(id)

    if request.method == 'POST':
        body = request.form['body']
        db = get_db()
        db.execute(
            'UPDATE answer SET body = ?'
            ' WHERE id = ?',
            (body, id)
        )
        db.commit()
        return redirect(url_for('question.que', id=post['qid']))

    return render_template('question/updateanswer.html', post=post)

@bp.route('/<int:id>/deleteanswer', methods=('POST',))
@login_required
def deleteanswer(id):
    q = get_answer(id)
    db = get_db()
    db.execute('DELETE FROM answer WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('question.que', id=q['qid']))