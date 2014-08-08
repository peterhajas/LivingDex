from flask import session
import csv

currentUsers = {}

class User:
    def __init__(self):
        self.username = ''
        self.password = ''
        self.friendCode = ''
        self.pokemon  = []

''' Database Reading and Writing '''

def loadDatabase(path):
    with open(path, 'rb') as databaseFile:
        reader = csv.reader(databaseFile, delimiter=' ', quotechar='|')
        for row in reader:
            userForRow = User()
            userForRow.username = row[0]
            userForRow.password = row[1]
            userForRow.friendCode = row[2]

            for pokemon in range(3, len(row)):
                userForRow.pokemon.append(int(pokemon))

            currentUsers[userForRow.username] = userForRow

def writeDatabase(path):
    with open(path, 'wb') as databaseFile:
        writer = csv.writer(databaseFile, delimiter=' ', quotechar='|')
        
        for username in currentUsers.keys():
            userForRow = currentUsers[username]

            row = [username, userForRow.password, userForRow.friendCode]
            row = row + userForRow.pokemon
            writer.writerow(row)

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

def registerUser(username, password, friendCode):
    newuser = User()
    newuser.username = username
    newuser.password = password
    newuser.friendCode = friendCode

    currentUsers[username] = newuser

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
    writeDatabase('test.csv')

def userHasPassword(username, password):
    if username in currentUsers.keys():
        return password == currentUsers[username].password
    else:
        return False

