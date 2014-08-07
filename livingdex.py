from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect

from users import *

app = Flask(__name__)

init()

@app.route('/')
def home():
    return 'Welcome to LivingDex'

@app.route('/user/<username>')
def user(username):
    return render_template('user.html', username=username, dex=dexForUsername(username), loggedIn=userIsLoggedIn(username))

@app.route('/togglePokemon', methods=['POST'])
def togglePokemon():
    username = request.form['username']
    toggledPokemon = request.form['toggledPokemon']
    print toggledPokemon
    if username == currentUser():
        togglePokemonForCurrentUser(int(toggledPokemon))
    return 'OK'

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = 'no error'
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if userHasPassword(username, password):
            logInUser(username)
            return redirect(url_for('user', username=username))
        else:
            error = 'Bad username / password'
    return render_template('login.html')

if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    # app.run()
    app.run(host='0.0.0.0', debug = True)

