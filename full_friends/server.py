from flask import Flask, redirect, request, render_template
from mysqlconnection import MySQLConnector

app = Flask (__name__)
mysql = MySQLConnector (app, 'friendsdb')

@app.route ('/')
def index():
    query = 'SELECT * FROM friends'
    friends = mysql.query_db (query)
    print friends
    return render_template ('index.html', friends = friends)

@app.route ('/process', methods=['POST'])
def process ():
    name = request.form['name'].split( )
    data = {
        'first_name' : name[0],
        'last_name' : name[1],
        'age' : request.form['age']
    }
    query = "INSERT INTO friends (first_name, last_name, age, created_at, updated_at)  VALUES (:first_name, :last_name, :age, NOW(), NOW())"
    mysql.query_db (query, data)
    return redirect('/')

app.run (debug = True)