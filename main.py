from flask import Flask, render_template, jsonify, session
from flask import request, redirect, g, url_for
import mysql.connector
import hashlib
import json
import time
import users
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def initialize():
    return app.send_static_file('login.html')

@app.route("/signup")
def signup():
    return app.send_static_file('index.html')

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

    return app.send_static_file('login.html')

@app.route('/protected')
def protected():
    if g.user:
        return render_template('protected.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return app.send_static_file('login.html')


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
        return '<html><body><h1>Registration Successful</h1></body></html>'
    
if __name__ == "__main__":
    print ("starting server")
    app.run(host="127.0.0.1", port=1234)
    

