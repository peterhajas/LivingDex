from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect

from users import *

app = Flask(__name__)

loadDatabase('test.csv')

@app.route('/')
def home():
    return 'Welcome to LivingDex'

@app.route('/user/<username>')
def user(username):
    return render_template('user.html', username=username, dex=dexForUsername(username))

@app.route('/togglePokemon', methods=['POST'])
def togglePokemon():
    username = request.form['username']
    if username == currentUser():
        toggledPokemon = request.form['toggledPokemon']
        togglePokemonForCurrentUser(int(toggledPokemon))
    return 'OK'

@app.route('/register', methods=['POST'])
def register():
    error = ''
    registerUsername = request.form['registerUsername']
    registerPassword = request.form['registerPassword']

    if len(registerUsername) > 0:
        registerUser(registerUsername, registerPassword, 0)
        logInUser(registerUsername)
        return redirect(url_for('user', username=registerUsername))

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = ''
    if request.method == 'POST':
        loginUsername = request.form['loginUsername']
        loginPassword = request.form['loginPassword']

        if len(loginUsername) > 0:
            if userHasPassword(username, password):
                logInUser(username)
                return redirect(url_for('user', username=username))
            else:
                error = 'Bad username / password'
        else:
            error = 'You need to enter in a username and password to register or log in as.'

    return render_template('login.html')

@app.route('/logout')
def logoutAndGoHome():
    logout()
    return home()

if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    # app.run()
    app.run(host='0.0.0.0', debug = True)

