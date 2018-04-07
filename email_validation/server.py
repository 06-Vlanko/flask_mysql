from flask import Flask, render_template, request, redirect, flash
from mysqlconnection import MySQLConnector
import re

app = Flask (__name__)
mysql = MySQLConnector (app, 'email_validation')
app.secret_key = 'supersecret!'

#used to verify if the email has the form some@something.com, use with EMAIL_REGEX.match(email)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route ('/')
def index ():
    return render_template ('index.html')

@app.route ('/process', methods = ['POST'])
def process ():
    data = {
        'email_address': request.form['email']
    }

    if not EMAIL_REGEX.match(data['email_address']):
        flash ('The email you entered is invalid')
        return redirect ('/')

    query = 'SELECT id from emails WHERE email_address = :email_address'

    query_result = mysql.query_db (query, data)

    if query_result:
        flash ('Email is already in the database!')
        return redirect ('/')
    else:
        query = 'INSERT INTO emails (email_address, created_at, updated_at) VALUES (:email_address, NOW(), NOW())'
        mysql.query_db (query, data)
        return redirect ('/success')

@app.route ('/success')
def sucess ():
    query = 'SELECT email_address, created_at FROM emails'
    query_result = mysql.query_db (query)
    return render_template ('sucess.html', query_result=query_result)

app.run (debug=True)