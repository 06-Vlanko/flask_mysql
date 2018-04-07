from  flask import Flask, render_template, redirect, request, flash, session
from mysqlconnection import MySQLConnector
import re, os, binascii, md5

app = Flask (__name__)
app.secret_key = 'topsecret'
mysql = MySQLConnector (app, 'the_wall')

#used to verify if the email has the form some@something.com, use with EMAIL_REGEX.match(email)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route ('/')
def index ():
    if session.get('id'):
        return redirect ('/wall')

    return render_template ('index.html')

@app.route ('/login', methods=['POST'])
def login ():

    data = {
        'email': request.form['log_email'],
        'password': request.form['log_password']
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
            session ['user_id'] = query_result[0]['id']
            session ['first_name'] = query_result[0]['first_name']
            session ['last_name'] = query_result[0]['last_name']

            print '----> PASSWORDS ARE THE SAME'
            
            return redirect ('/wall')
            
        else:
            print '----> PASSWORDS MISSMATCH'
            #if the passwords do not match, redirect to login form (index) with errors
            flash ('The email or password that you entered is incorrect, please try again')
            return redirect ('/')
    else:
        print '----> REGISTRATION NEEDED'
        #if the user does not exists (no matching email)
        flash ('The user you entered does not exists, please register to continue')
        return redirect ('/')#CHANGE

    return redirect ('/')

@app.route ('/register', methods=['POST'])
def register():
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
    print '----------------------------------'
    print data
    print '----------------------------------'
    flag = False #flag to determine if redirect is needed due to user errors

    #checks that the first name is at least two characters
    if len(data['first_name'])<2:
        flag = True
        flash ('The "First Name" field must be at least two characters')
    else: #verifies if all characters in first_name are letters
        for character in data['first_name']:
            if not character.isalpha():
                flag = True
                flash ('The "First Name" field should only contain letters')
                break #cuz only one character not being a letter will make the user submission invalid
    
    #checks that the last name is at least two characters
    if len(data['last_name'])<2:
        flag = True
        flash ('The "Last Name" field must be at least two characters')
    else: #verifies if all characters in last_name are letters
        for character in data['last_name']:
            if not character.isalpha():
                flag = True
                flash ('The "Last Name" field should only contain letters')
                break #cuz only one character not being a letter will make the user submission invalid
    
    print '-----> VERYFYING EMAIL'
    #checks if the email fields is empty
    if len(data['email'])<1:
        flag = True
        flash ('The "Email" field cannot be empty')
    #checks if the email is in the format something@something.some
    elif not EMAIL_REGEX.match(data['email']):
        flag = True
        flash ("Invalid email address")
    #checks if the email is already in use in the database
    query = 'SELECT email FROM users WHERE email = :email'
    if mysql.query_db(query, data):
        flash ('The email you entered is already in use, please sign in or use a different email')
        return redirect ('/')

    print '-----> VERYFYING PASSWORD'
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
                print '-----> THE PASSWORDS ENTERED DOES NOT MATCH THE DATABASE!'
                flash ('The password and confirm password values should match')
                break #stops verifying if a single character is different
                
    print '-----> THE PASSWORDS ARE THE SAME, ALL CHECKS COMPLETED!'
    #redirects back to the form if any of the previous checks was missed (flag = True)
    if flag:
        flag = True
        print '-----> REDIRECTING CUZ USER ERROR'
        return redirect ('/')#CHANGE
    else: #redirects to the success page if all info is correct
        print '-----> NO ERRORS ON REGISTRATION FORM, SENDING INFO TO DATABASE'
        data['password'] = md5.new(data['password'] + data['salt']).hexdigest()

        query = 'INSERT INTO users (first_name, last_name, email, password, salt, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, :salt, NOW(), NOW() )'

        #submits the query to insert a new user with the data from the register form
        #data ['id'] = 

        #starts the session (cuz we are now logged in)
        print '-----> INITIALIZING SESSION'
        session ['user_id'] = mysql.query_db (query, data)
        session ['first_name'] = data['first_name']
        session ['last_name'] = data['last_name']
        print '-----> CURRENT SESSION DATA:'
        print session
        print '-----> REDIRECTING TO /WALL'
        return redirect ('/wall')

    # return render_template ('success.html') #CHANGE
    # return redirect ('/register')
    return redirect ('/')

@app.route ('/wall')
def wall():
    #verfies if there is an active session
    if not session.get('user_id'):
        flash ('Please log in or register!')
        return redirect ('/')
    #query to get all the messages from all users
    query = 'SELECT users.id, users.first_name, users.last_name, messages.id, messages.message, messages.created_at FROM users JOIN messages ON users.id = messages.user_id ORDER BY created_at DESC'
    #saves the list of messages
    messages = mysql.query_db(query)
    print '-----COLLECTION OF MSGS-----'
    print messages

    #query to get the comments from all users for all messages
    query = 'SELECT users.first_name, users.last_name, comments.comment, message_id, comments.created_at FROM users JOIN comments ON users.id = comments.user_id ORDER BY created_at ASC'
    comments = mysql.query_db(query)
    #renders the template passing the list of messages
    return render_template ('wall.html', messages=messages, comments=comments)

@app.route('/post_message', methods=['POST'])
def post ():
    data = {
        'message': request.form['message'],
        'user_id': session ['user_id']
    }

    print '---------NEW MESSAGE----------'
    print data
    print '-----------SESSION------------'
    print session

    #checks that the message box is not empty
    if len(data['message'])<1:
        flash ('Please write a message before submitting')
        return redirect ('/wall')
    
    query = 'INSERT INTO messages (user_id, message, created_at, updated_at) VALUES (:user_id, :message, NOW(), NOW())'
    #adds the new message to the database
    mysql.query_db (query, data)

    return redirect ('/wall')

@app.route ('/post_comment', methods=['POST'])
def postComment ():
    #gathers the data to pass to the database
    data = {
        'user_id': session['user_id'],
        'message_id': request.form['message_id'],
        'comment': request.form['comment']
    }
    print '---------NEW COMMENT----------'
    print data
    #query to insert a new comment
    query = 'INSERT INTO comments (user_id, message_id, comment, created_at, updated_at) VALUE (:user_id, :message_id, :comment, NOW(), NOW() )'
    
    #sends the query to the database
    print '-----> COMMENT ID:', mysql.query_db (query, data)

    return redirect ('/wall')

@app.route ('/logout')
def logOut ():
    session.clear()
    print '----> SESSION CLEARED:', session
    return redirect ('/')

app.run (debug=True)