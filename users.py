import string
import sys
import user

def enum(**enums):
    return type('Enum', (), enums)

# This enum specifies the captured state of a Pokemon
# 0 is the user hasn't caught the Pokemon
# 1 is the user has caught the Pokemon

CapturedState = enum(Uncaught = 0, Caught = 1)

# This enum specifies the comparison state (between two users) of a Pokemon
# 0 means neither user has caught the Pokemon
# 1 means the first user has caught the Pokemon
# 2 means the second user has caught the Pokemon
# 3 means both users have caught the Pokemon

ComparisonResult = enum(NeitherCaught = 0, FirstCaught = 1, SecondCaught = 2, BothCaught = 3)

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
        friendCode = self._validatedFriendCode(friendCode)
        validCharacters = string.digits
        if not self._verifyStringContainsCharactersFromList(friendCode, validCharacters):
            return (False, "A friend code may only contain digits")
        elif len(friendCode) > 16:
            return (False, "A friend code is 16 numbers")
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
        newuser = user.User()
        newuser.username = username
        newuser.password = password
        newuser.friendCode = self._validatedFriendCode(friendCode)

        db.session.add(newuser)
        db.session.commit()

    ''' User Access and Query '''

    def userForUsername(self, username):
        foundUser = user.User.query.filter_by(username=username).first()
        return foundUser

    def userExists(self, username):
        return self.userForUsername(username) is not None

    def pokemonCaughtForUser(self, user):
        unicodePokemon = user.pokemon
        return unicodePokemon

    def dexForUser(self, user, pokemonCount):
        dex = self.pokemonCaughtForUser(user)
        dex = dex[:pokemonCount]
        return dex

    def comparisonResultBetweenUsers(self, user1, user2, pokemonIndex):
        # Why +1? Because these indexes are 0-indexed, but
        # _stateOfPokemonForUser assumes logical indices
        logicalPokemonIndex = pokemonIndex+1
        stateForUser1 = self._stateOfPokemonForUser(user1, logicalPokemonIndex)
        stateForUser2 = self._stateOfPokemonForUser(user2, logicalPokemonIndex)

        if stateForUser1 == CapturedState.Uncaught:
            if stateForUser2 == CapturedState.Uncaught:
                return ComparisonResult.NeitherCaught
            else:
                return ComparisonResult.SecondCaught
        if stateForUser1 == CapturedState.Caught:
            if stateForUser2 == CapturedState.Uncaught:
                return ComparisonResult.FirstCaught
            else:
                return ComparisonResult.BothCaught

        # We need a better error case, but -1 will do for now
        return -1
    
    def comparedDexBetweenUsers(self, user1, user2, pokemonCount):
        comparedDex = []

        for i in range(pokemonCount):
            comparisonResult = self.comparisonResultBetweenUsers(user1, user2, i)

            newStatus = unicode(comparisonResult)
            comparedDex.append(newStatus)

        comparedDex = "".join(comparedDex)

        return comparedDex

    def _setStateForPokemonForUser(self, user, pokemon, state, db):
        pokemon = pokemon - 1
        dex = self.pokemonCaughtForUser(user)
        dex = list(dex)

        dex[pokemon] = state

        dex = "".join(dex)
        user.pokemon = dex

        db.session.commit()

    def _stateOfPokemonForUser(self, user, pokemon):
        pokemon = pokemon - 1
        dex = self.pokemonCaughtForUser(user)
        dex = list(dex)
        dexState = dex[pokemon]

        if int(dexState) == 0:
            return CapturedState.Uncaught
        else:
            return CapturedState.Caught

    def catchPokemonForUser(self, user, pokemon, db):
        self._setStateForPokemonForUser(user, pokemon, u'1', db)
    
    def uncatchPokemonForUser(self, user, pokemon, db):
        self._setStateForPokemonForUser(user, pokemon, u'0', db)

    def changeFriendCodeForUser(self, username, friendCode, db):
        friendCode = self._validatedFriendCode(friendCode)
        if self.verifyNewFriendCode(friendCode)[0] is not False:
            user = self.userForUsername(username)
            user.friendCode = friendCode
            db.session.commit()

    def userHasPassword(self, username, password):
        if self.userExists(username):
            return password == self.userForUsername(username).password
        else:
            return False

