from flask import session

def logInUser(username):
    session['username'] = username

def logout():
    session['username'] = None

def currentUser():
    return session['username']

def userIsLoggedIn(username):
    return currentUser() == username
