import string
from livingdex import User

class UserDatabase:
    def __init__(self):
        pass

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
        elif len(username) > 20:
            return (False, "Username is too long. Must be 20 characters or less")
        elif not self._verifyStringisASCII(username):
            return (False, "A username may only contain uppercase, lowercase and digits")
        else:
            return (True, None)
    
    def verifyNewPassword(self, password):
        if not self._verifyStringisASCII(password):
            return (False, "A password may only contain uppercase, lowercase and digits")
        if len(password) == 0:
            return (False, "You need to have a password that's at least one character. But don't make it just one character, that's insecure.")
        elif len(password) > 20:
            return (False, "Password is too long. Must be 20 characters or less")
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

    def displayFriendlyFriendCodeForFriendCode(self, friendCode):
        displayFriendlyFriendCode = ''
        
        for i in range(len(friendCode)):
            if i % 4 == 0 and i is not 0:
                displayFriendlyFriendCode = displayFriendlyFriendCode + '-'
            displayFriendlyFriendCode = displayFriendlyFriendCode + friendCode[i]

        return displayFriendlyFriendCode

    def registerUser(self, username, password, friendCode, db):
        newuser = User()
        newuser.username = username
        newuser.password = password
        newuser.friendCode = self._validatedFriendCode(friendCode)

        db.session.add(newuser)
        db.session.commit()

    ''' User Access and Query '''

    def userForUsername(self, username):
        user = User.query.filter_by(username=username).first()
        return user

    def userExists(self, username):
        return self.userForUsername(username) is not None

    def pokemonCaughtForUser(self, user):
        unicodePokemon = user.pokemon
        return unicodePokemon

    def dexForUser(self, user, pokemonCount):
        dex = self.pokemonCaughtForUser(user)
        dex = dex[:pokemonCount]
        return dex

    def togglePokemonForUser(self, user, pokemon, db):
        pokemon = pokemon - 1
        dex = self.pokemonCaughtForUser(user)
        dex = list(dex)

        caughtStatus = dex[pokemon]
        newStatus = caughtStatus

        if caughtStatus == u'0':
            newStatus = u'1'
        elif caughtStatus == u'1':
            newStatus = u'0'

        dex[pokemon] = newStatus
        dex = "".join(dex)
        user.pokemon = dex

        db.session.commit()

    def userHasPassword(self, username, password):
        if self.userExists(username):
            return password == self.userForUsername(username).password
        else:
            return False

