from  flask import Flask, render_template, redirect, request, flash, session
from mysqlconnection import MySQLConnector
import re, os, binascii, md5

app = Flask (__name__)
app.secret_key = 'topsecret'
mysql = MySQLConnector (app, 'users_db')

#used to verify if the email has the form some@something.com, use with EMAIL_REGEX.match(email)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route ('/')
def index ():
    if session.get('id'):
        return redirect ('/success')
    return render_template ('index.html')

@app.route ('/login', methods=['POST'])
def login ():
    data = {
        'email': request.form['email'],
        'password': request.form['password']
    }
    
    #hashes the password

    #flag used to control wether or not redirect to login form (index) is required
    flag = False

    #checks the length of email and if it is a valid email
    if len(data['email']) <1:
        flash ('The email field cannot be empty')
        flag = True
    elif not EMAIL_REGEX.match(data['email']):
        flash ('The email you entered is invalid')
        flag = True
    
    #checks the length of the password
    if len(data['password']) <1:
        flash ('The password field cannot be empty')
        flag = True

    #if there are issues with the password or the email, redirect to index for another login attempt
    if flag:
        return redirect ('/')
    
    #if no issues where found:
    #checks if the email exists in the database
    query = 'SELECT * FROM users WHERE email = :email'
    query_result = mysql.query_db (query, data)
    
    #if there is a users with the entered email (query response is not empty) then 
    if query_result:
        #hashes the entered password with the salt from the database
        data['password']=md5.new(data['password'] + query_result[0]['salt']).hexdigest()
        #check if the passwords match
        if data['password'] == query_result[0]['password']:
            #if they do, sent to success page!
            flash ('Succesfully logged in!')
            session ['id'] = query_result[0]['id']
            session ['first_name'] = query_result[0]['first_name']
            session ['last_name'] = query_result[0]['last_name']
            session ['registered_at'] = query_result[0]['created_at']

            print '----> PASSWORDS ARE THE SAME'
            
            return redirect ('/success')
            
        else:
            print '----> PASSWORDS ARE THE >>NOT<< SAME'
            #if the passwords do not match, redirect to login form (index) with errors
            flash ('The password you entered is incorrect, please try again')
            return redirect ('/')
    else:
        print '----> REGISTRATION NEEDED'
        #if the user does not exists (no matching email)
        return redirect ('/register')

@app.route ('/register')
def register ():
    return render_template ('register.html')

@app.route ('/add_user', methods = ['POST'])
def add_user():
    print 'adding user'
    #dictionary to hold the values the user is entering (to be sent to sql later)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirm_password': request.form['confirm_password'],
        'salt': binascii.b2a_hex(os.urandom(15))
    }

    flag = False #flag to determine if redirect is needed due to user errors

    #checks that the first name is at least two characters
    if len(data['first_name'])<=2:
        flag = True
        flash ('The "First Name" field must be at least two characters')
    else: #verifies if all characters in first_name are letters
        for character in data['first_name']:
            if not character.isalpha():
                flag = True
                flash ('The "First Name" field should only contain letters')
                break #cuz only one character not being a letter will make the user submission invalid
    
    #checks that the last name is at least two characters
    if len(data['last_name'])<=2:
        flag = True
        flash ('The "Last Name" field must be at least two characters')
    else: #verifies if all characters in last_name are letters
        for character in data['last_name']:
            if not character.isalpha():
                flag = True
                flash ('The "Last Name" field should only contain letters')
                break #cuz only one character not being a letter will make the user submission invalid
    
    #checks if the email fields is empty
    if len(data['email'])<1:
        flag = True
        flash ('The "Email" field cannot be empty')
    #checks if the email is in the format something@something.some
    elif not EMAIL_REGEX.match(data['email']):
        flag = True
        flash ("Invalid email address")

    #checks that the entered password is at least 8 characters
    if len(data['password'])<8:
        flag = True
        flash ('The "Password" must be at least 8 characters')
    
    #checks that the password and confirm_password lengths match
    if len(data['password']) != len(data['confirm_password']):
        flag = True
        flash ('The password and confirm password values should match')
    else: #if the lengths match, check if characters are an exact match
        for index in range ( len(data['password']) ):
            if data['password'][index] != data['confirm_password'][index]:
                flag = True
                flash ('The password and confirm password values should match')
                break #stops verifying if a single character is different

    #redirects back to the form if any of the previous checks was missed
    if flag:
        flag = True
        print 'redirecting cuz missing'
        return redirect ('/register')
    else: #redirects to the succes page if all info is correct
        print 'redirecting with success'
        data['password'] = md5.new(data['password'] + data['salt']).hexdigest()

        query = 'INSERT INTO users (first_name, last_name, email, password, salt, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, :salt, NOW(), NOW() )'

        mysql.query_db (query, data)
        flash ('Success!!!'+ data['password'])
        return redirect ('/success')

    return render_template ('success.html')
    return redirect ('/register')

@app.route ('/success')
def success ():

    return render_template ('success.html')

@app.route ('/logout')
def logOut ():
    session.clear()
    print '----> SESSION', session
    return redirect ('/')

#def verifyEmail (string):
app.run (debug=True)

