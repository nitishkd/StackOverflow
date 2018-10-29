from flask import Flask, render_template, jsonify
from flask import request
import mysql.connector
import hashlib
import json
import time
import users

app = Flask(__name__)


@app.route("/")
def initialize():
    return app.send_static_file('index.html')


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


