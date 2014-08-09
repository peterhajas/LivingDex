from flask import session
import csv

class User:
    def __init__(self):
        self.username = ''
        self.password = ''
        self.friendCode = ''
        self.pokemon  = []

class UserDatabase:
    def __init__(self, pathToDatabase):
        self.users = {}
        self.pathToDatabase = pathToDatabase
        self.loadDatabase()

    ''' Database Reading / Writing '''

    def loadDatabase(self):
        with open(self.pathToDatabase, 'rb') as databaseFile:
            reader = csv.reader(databaseFile, delimiter=' ', quotechar='|')
            for row in reader:
                userForRow = User()
                userForRow.username = row[0]
                userForRow.password = row[1]
                userForRow.friendCode = row[2]

                for pokemon in range(3, len(row)):
                    userForRow.pokemon.append(int(pokemon))

                self.users[userForRow.username] = userForRow

    def writeDatabase(self):
        with open(self.pathToDatabase, 'wb') as databaseFile:
            writer = csv.writer(databaseFile, delimiter=' ', quotechar='|')
            
            for username in self.users.keys():
                userForRow = self.users[username]

                row = [username, userForRow.password, userForRow.friendCode]
                row = row + userForRow.pokemon
                writer.writerow(row)

    ''' Adding Users '''

    def registerUser(self, username, password, friendCode):
        newuser = User()
        newuser.username = username
        newuser.password = password
        newuser.friendCode = friendCode

        self.users[username] = newuser

    ''' User Access and Query '''

    def userForUsername(self, username):
        if username not in self.users.keys():
            return None
        else:
            return self.users[username]

    def userExists(self, username):
        return self.userForUsername(username) is not None

    def pokemonCaughtForUsername(self, username):
        return self.userForUsername(username).pokemon

    def dexForUsername(self, username):
        pokemonCaught = self.pokemonCaughtForUsername(username)
        dex = [0] * 10
        for pokemon in pokemonCaught:
            #-1 because our list of Pokemon is 1-indexed
            dex[pokemon-1] = 1
        return dex

    def togglePokemonForUser(self, username, pokemon):
        currentPokemon = self.userForUsername(username).pokemon
        if pokemon in currentPokemon:
            currentPokemon.remove(pokemon)
        else:
            currentPokemon.append(pokemon)
        self.writeDatabase()

    def userHasPassword(self, username, password):
        if username in self.users.keys():
            return password == self.users[username].password
        else:
            return False


''' User Login '''

def logInUser(username):
    session['username'] = username

def logout():
    session['username'] = None

def currentUser():
    return session['username']

def userIsLoggedIn(username):
    return currentUser() == username

