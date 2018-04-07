from  flask import Flask, render_template, redirect, request, flash, session
from mysqlconnection import MySQLConnector
import re, os, binascii, md5

app = Flask (__name__)
app.secret_key = 'topsecret'
mysql = MySQLConnector (app, 'friendsdb')

@app.route ('/users')
def index():
    query = 'SELECT id, first_name, last_name, created_at FROM friends'
    query_result = mysql.query_db (query)

    return render_template ('index.html', users=query_result)

@app.route ('/users/new')
def new ():
    return render_template ('new_user.html')

app.run (debug=True)