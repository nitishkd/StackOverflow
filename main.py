from flask import Flask, render_template, jsonify, session
from flask import request, redirect, g, url_for
import mysql.connector
import hashlib
import json
import time
import users
import os
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_pyfile('config.cfg')

mail = Mail(app)

S = URLSafeTimedSerializer('dasfegrhrdaUYUHHNJ&@IUJ')

@app.route("/")
def initialize():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        passwd = request.form['password']
        upasswd = hashlib.sha1(passwd.encode()).hexdigest()
        print (upasswd)
        if upasswd == users.getPassword(request.form['username']):
            session['user'] = request.form['username']
            return redirect(url_for('protected'))

    return render_template('index.html')

@app.route('/protected')
def protected():
    if g.user:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('index.html')


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@app.route("/register", methods=['POST'])
def register(): 
    usermail= request.form['usermail']
    username = request.form['username']
    passwd = request.form['passwd']
    alias = "user" + str(int(time.time()))
    upasswd = hashlib.sha1(passwd.encode()).hexdigest()
    resp = users.addusers(username, alias, usermail, upasswd)
    if(resp == -1):
        return '<html><body><h1>Registration failed</h1></body></html>'
    else:
        token = S.dumps(usermail, salt='email-confirm')
        msg = Message('Confirm Email', sender="stackoverflow.iiith@gmail.com", recipients=[usermail])
        link = url_for('confirm_mail', token=token, _external=True)
        msg.body = 'Your Authentication link is : {}'.format(link)
        mail.send(msg)
        return '<html><body><h1>Registration Successful. Token is {} </h1></body></html>'.format(token)


@app.route('/confirm/<token>')
def confirm_mail(token):
    try:
        email = S.loads(token, salt='email-confirm', max_age=3600)
        users.email_confirmation(email) 
        return render_template('index.html')

    except SignatureExpired:
        return "<h1> Token Expired !<h1>"


if __name__ == "__main__":
    print ("starting server")
    app.run(host="127.0.0.1", port=1234, debug=True)
    

