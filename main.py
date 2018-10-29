from flask import Flask, render_template, jsonify
from flask import request
import mysql.connector
import hashlib
import json
import time

app = Flask(__name__)


@app.route("/")
def initialize():
    return render_template('index.html')


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/register", methods=['POST'])
def register(): 
    usermail= request.form['usermail']
    username = request.form['username']
    passwd = request.form['passwd']
    alias = "user" + str(int(time.time()))
    upasswd = hashlib.sha1(passwd.encode()).hexdigest()
    
    database = mysql.connector.connect(host="localhost",user="newuser",passwd="password")
    cursor = database.cursor()
    sql = "INSERT INTO stackoverflow.users (username, alias, useremail, userpass, userrating) VALUES (%s, %s, %s, %s, %s)"
    val = (username, alias , usermail, upasswd, 0)

    cursor.execute(sql,val)
    database.commit()
    database.disconnect()

if __name__ == "__main__":
    print ("starting server")
    app.run(host="127.0.0.1", port=1234,debug=True)


