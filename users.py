from flask import session

currentUsers = {}

class User:
    def __init__(self):
        self.username = ''
        self.password = ''
        self.pokemon  = []

''' Test data '''
def init():
    peter = User()
    peter.username = 'phajas'
    peter.password = 'test'
    peter.pokemon  = [1,2,3]
    addUser(peter)

    eric = User()
    eric.username = 'eric'
    eric.password = 'lol'
    eric.pokemon = [4,5,6]
    addUser(eric)

    alex = User()
    alex.username = 'alex'
    alex.password = 'password'
    alex.pokemon = [1,2,7,8,9]
    addUser(alex)

''' User Login '''

def logInUser(username):
    session['username'] = username

def logout():
    session['username'] = None

def currentUser():
    return session['username']

def userIsLoggedIn(username):
    return currentUser() == username

''' User Modification '''

def addUser(user):
    if userForUsername(user.username) is not None:
        pass
    else:
        currentUsers[user.username] = user

''' User Access and Query '''

def userForUsername(username):
    if username not in currentUsers.keys():
        return None
    else:
        return currentUsers[username]

def pokemonCaughtForUsername(username):
    return userForUsername(username).pokemon

def dexForUsername(username):
    pokemonCaught = pokemonCaughtForUsername(username)
    dex = [0] * 10
    for pokemon in pokemonCaught:
        #-1 because our list of Pokemon is 1-indexed
        dex[pokemon-1] = 1
    return dex

def togglePokemonForCurrentUser(pokemon):
    currentPokemon = userForUsername(currentUser()).pokemon
    if pokemon in currentPokemon:
        currentPokemon.remove(pokemon)
    else:
        currentPokemon.append(pokemon)
    print currentPokemon

def userHasPassword(username, password):
    if username in currentUsers.keys():
        return password == currentUsers[username].password
    else:
        return False

