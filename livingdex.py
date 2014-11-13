import sys, os

from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect

from flask.ext.sqlalchemy import SQLAlchemy

from usersession import *
from pokedex import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:////tmp/test.db')

if app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:////tmp/test.db':
    app.config['DEBUG'] = True

db = SQLAlchemy(app)

number_of_pokemon_str_entries = 1000

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    friendCode = db.Column(db.String(16))
    pokemon = db.Column(db.String(number_of_pokemon_str_entries))
    def __init__(self):
        self.username = ''
        self.password = ''
        self.friendCode = ''
        self.pokemon  = '0' * number_of_pokemon_str_entries

    def __repr__(self):
        return '<Username %r>' % self.username

from users import *

db.create_all()
db.session.commit()

database = UserDatabase()
nationalDex = NationalDex('pokesprite/data/pkmn.json')

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/user/<username>')
def user(username):
    if database.userExists(username):
        user = database.userForUsername(username)
        friendCode = user.friendCode
        friendCode = database.displayFriendlyFriendCodeForFriendCode(friendCode)
        dex = database.dexForUser(user, nationalDex.numberOfPokemon)
        pokemonNames = nationalDex.pokemonNames
        pokemonSlugs = nationalDex.pokemonSlugs

        return render_template('user.html', username=username, friendCode=friendCode, dex=dex, pokemonNames=pokemonNames, pokemonSlugs=pokemonSlugs)
    else:
        return render_template('baduser.html', username=username)

@app.route('/compare/<username1>/<username2>')
def compareUsers(username1, username2):
    if database.userExists(username1) and database.userExists(username2):
        user1 = database.userForUsername(username1)
        user2 = database.userForUsername(username2)

        comparedDex = database.comparedDexBetweenUsers(user1, user2, nationalDex.numberOfPokemon)

        pokemonNames = nationalDex.pokemonNames
        pokemonSlugs = nationalDex.pokemonSlugs

        return render_template('compare.html', username1=username1, username2=username2, comparedDex=comparedDex, pokemonNames=pokemonNames, pokemonSlugs=pokemonSlugs)
    else:
        return render_template('baduser.html', username=username1) # TODO: plh: write a special error page for this

@app.route('/togglePokemon', methods=['POST'])
def togglePokemon():
    username = request.form['username']
    if username == currentUser():
        toggledPokemon = request.form['toggledPokemon']
        user = database.userForUsername(username)
        database.togglePokemonForUser(user, int(toggledPokemon), db)
    return 'OK'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return redirect(url_for('login'))
    registerUsername = request.form['registerUsername']
    registerPassword = request.form['registerPassword']
    registerFriendCode = request.form['registerFriendCode']

    usernameIsValid, usernameError = database.verifyNewUsername(registerUsername)
    passwordIsValid, passwordError = database.verifyNewPassword(registerPassword)
    friendCodeIsValid, friendCodeError = database.verifyNewFriendCode(registerFriendCode)

    if not usernameIsValid:
        return render_template('login.html', error=usernameError)
    elif not passwordIsValid:
        return render_template('login.html', error=passwordError)
    elif not friendCodeIsValid:
        return render_template('login.html', error=friendCodeError)
    else:
        database.registerUser(registerUsername, registerPassword, registerFriendCode, db)
        logInUser(registerUsername)
        return redirect(url_for('user', username=registerUsername))

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        loginUsername = request.form['loginUsername']
        loginPassword = request.form['loginPassword']

        if len(loginUsername) > 0:
            if not database.userExists(loginUsername):
                error = 'User {} does not exist'.format(loginUsername)
            elif database.userHasPassword(loginUsername, loginPassword):
                logInUser(loginUsername)
                return redirect(url_for('user', username=loginUsername))
            else:
                error = 'Incorrect username / password'
        else:
            error = 'You need to enter in a username and password to register or log in as.'

    return render_template('login.html', error=error)

@app.route('/logout')
def logoutAndGoHome():
    logout()
    return home()

