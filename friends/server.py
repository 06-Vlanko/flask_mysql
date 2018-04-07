from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector

app = Flask(__name__)
mysql = MySQLConnector(app,'friendsdb')

@app.route('/')
def index():
    friends = mysql.query_db("SELECT * FROM friends")
    #print friends
    return render_template('index.html', friends=friends)

@app.route ('/friends/<friend_id>')
def show (friend_id):
    data = { 'id' : friend_id }
    query = 'SELECT * FROM friends WHERE id = :id'
    friends = mysql.query_db (query, data)
    return render_template ('index.html', friends = friends)

@app.route('/friends', methods=['POST'])
def create():
    data =  {
             'first_name': request.form['first_name'],
             'last_name':  request.form['last_name'],
             'occupation': request.form['occupation']
            }
    
    query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (:first_name, :last_name, :occupation, NOW(), NOW())"
    
    mysql.query_db (query, data)

    return redirect('/')
app.run(debug=True)