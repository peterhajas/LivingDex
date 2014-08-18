import csv
import string

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
            reader = csv.reader(databaseFile, delimiter=',', quotechar='|')
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
            writer = csv.writer(databaseFile, delimiter=',', quotechar='|')
            
            for username in self.users.keys():
                userForRow = self.users[username]

                row = [username, userForRow.password, userForRow.friendCode]
                row = row + userForRow.pokemon
                writer.writerow(row)

    ''' Adding Users '''

    def _verifyStringContainsCharactersFromList(self, stringToVerify, validCharacters):
        for character in stringToVerify:
            if character not in validCharacters:
                return False
        return True

    def _verifyStringisASCII(self, stringToVerify):
        validCharacters = string.ascii_letters + string.digits
        return self._verifyStringContainsCharactersFromList(stringToVerify, validCharacters)


    def verifyNewUsername(self, username):

        if self.userExists(username):
            return (False, "That username is already taken")
        elif len(username) == 0:
            return (False, "Username can't be empty")
        elif not self._verifyStringisASCII(username):
            return (False, "A username may only contain uppercase, lowercase and digits")
        else:
            return (True, None)
    
    def verifyNewPassword(self, password):
        if not self._verifyStringisASCII(password):
            return (False, "A password may only contain uppercase, lowercase and digits")
        if len(password) == 0:
            return (False, "You need to have a password that's at least one character. But don't make it just one character, that's insecure.")
        else:
            return (True, None)


    def verifyNewFriendCode(self, friendCode):
        validCharacters = string.digits + ' ' + '-'
        if not self._verifyStringContainsCharactersFromList(friendCode, validCharacters):
            return (False, "A friend code may only contain digits")
        else:
            return (True, None)

    def _validatedFriendCode(self, friendCode):
        friendCode = friendCode.encode('ascii', 'ignore')
        return friendCode.translate(None, ' -')

    def registerUser(self, username, password, friendCode):
        newuser = User()
        newuser.username = username
        newuser.password = password
        newuser.friendCode = self._validatedFriendCode(friendCode)

        self.users[username] = newuser
        self.writeDatabase()

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

    def dexForUsername(self, username, pokemonCount):
        pokemonCaught = self.pokemonCaughtForUsername(username)
        dex = [0] * pokemonCount
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

