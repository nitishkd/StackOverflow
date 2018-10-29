import mysql.connector
import json
import time

def checkuserexist(email):
    database = mysql.connector.connect(host="localhost",user="root",passwd="helloWORLD@123")
    cursor = database.cursor()
    cursor.execute("SELECT userid FROM stackoverflow.users where useremail= %s", (email,))
    data = cursor.fetchone()
    number_of_rows=cursor.rowcount
    if number_of_rows > 0 :
        return True
    else:
        return False

def addusers(username, alias, usermail, upasswd):
    database = mysql.connector.connect(host="localhost",user="root",passwd="helloWORLD@123")
    cursor = database.cursor()
    sql = "INSERT INTO stackoverflow.users (username, alias, useremail, userpass, userrating) VALUES (%s, %s, %s, %s, %s)"
    val = (username, alias , usermail, upasswd, 0)
    if checkuserexist(usermail):
        return -1
    else:
        affected_row = cursor.execute(sql,val)
        database.commit()
        return 1

