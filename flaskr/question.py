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
        tag=request.form['tag']
        print tag
        tags=tag.split(',')
        # s=string(tag)
        # print s
        error = None
        
        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (author_id,title,body)'
                ' VALUES (?, ?, ?)',
                ( g.user['id'],title, body)
            )
            x=db.execute( 'SELECT max(qid) as maximum FROM post').fetchone()
            data=db.execute("SELECT * FROM user WHERE id = ?", (g.user['id'],)).fetchone()
            print data
            flag=0
            if(data[3]>5):
                for i in tags:
                        db.execute(
                            'INSERT INTO qtags (tagname,qid)'
                            ' VALUES (?, ?)',
                            (i,x[0])
                        )
                        r=db.execute("SELECT * FROM tags WHERE tagname = ?", (i,)).fetchone()
                        if(r is None):
                            db.execute(
                            'INSERT INTO tags (tagname)'
                            ' VALUES (?)',
                            (i)
                            )

            else:
                for i in tags:
                    data=db.execute("SELECT * FROM tags WHERE tagname = ?", (i,)).fetchone()
                    if(data is None):
                        flag=1
                        break
                    else:
                        continue
                if(flag==0):
                    for i in tags:
                        db.execute(
                            'INSERT INTO qtags (tagname,qid)'
                            ' VALUES (?, ?)',
                            (i,x[0])
                        )
                else:
                    print "NO REPUTATION TO ADD TAGS"

            # print x['qid']
            #print x[0]
            
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
    tags=db.execute('SELECT * FROM qtags where qid=?',(id,)).fetchall()
    comments=db.execute('SELECT * FROM comment_question WHERE qid=?',(id,)).fetchall()
    ans=db.execute('SELECT * FROM answer WHERE qid = ?', (id,)).fetchall()
    ans_len=len(ans)
    comments_len=len(comments)
    tag_len=len(tags)
    return render_template('question/que.html',posts=posts,ans=ans,ans_len=ans_len,comments=comments,comments_len=comments_len,tags=tags,tag_len=tag_len)


@bp.route('/<int:id>/create_comment', methods=('GET', 'POST'))
@login_required
def create_comment(id):
    if request.method == 'POST':
        body = request.form['body']
        db = get_db()
        db.execute(
                'INSERT INTO comment_question(qid,author_id,body)'
                ' VALUES (?, ?, ?)',
                (id,g.user['id'], body)
            )
        db.commit()
        return redirect(url_for('question.que',id=id))

    return render_template('question/create_comment.html')


@bp.route('/<int:id>/upvote_question', methods=('GET', 'POST'))
@login_required
def upvote_question(id):
        db = get_db()
        result=db.execute('select * from upvote_que where qid=? and userid=?',(id,g.user['id'])).fetchone()
        if result is not None:
            if result[2]==2:
                db.execute('UPDATE upvote_que SET upvote_downvote=? WHERE qid = ? and userid=?',(1,id,g.user['id']))
                db.execute('UPDATE post SET upvotes= upvotes + 1 WHERE qid = ?',(id,))
        else:
            db.execute('insert into upvote_que(qid,userid,upvote_downvote) values(?,?,?)',(id,g.user['id'],1))          
            db.execute('UPDATE post SET upvotes=upvotes+1 WHERE qid = ?',(id,))
        db.commit()
        return redirect(url_for('question.que',id=id))


@bp.route('/<int:id>/downvote_question', methods=('GET', 'POST'))
@login_required
def downvote_question(id):
        db = get_db()
        result=db.execute('select * from upvote_que where qid=? and userid=?',(id,g.user['id'])).fetchone()
        if result is not None:
            if result[2]==1:
                db.execute('UPDATE upvote_que SET upvote_downvote=? WHERE qid = ? and userid=?',(2,id,g.user['id']))
                db.execute('UPDATE post SET upvotes=(upvotes-1) WHERE qid = ?',(id,))
        else:
            db.execute('insert into upvote_que(qid,userid,upvote_downvote) values(?,?,?)',(id,g.user['id'],2))
            db.execute('UPDATE post SET upvotes=(upvotes-1) WHERE qid = ?',(id,))    
        db.commit()
        return redirect(url_for('question.que',id=id)) 