import unittest
import user
from users import UserDatabase

class FakeDatabaseSession:
    def __init__(self):
        self.didCommit = False
        self.things = [ ]
    def commit(self):
        self.didCommit = True
    def add(self, thingToAdd):
        self.things.append(thingToAdd)

class FakeDatabase:
    def __init__(self):
        self.session = FakeDatabaseSession()

class TestUserOperations(unittest.TestCase):
    def setUp(self):
        self.userDB = UserDatabase()
        self.appDB = FakeDatabase()
        self.appDBSession = self.appDB.session

        self.register_ash()
        self.register_misty()
    def tearDown(self):
        self.userDB = None
        self.appDB = None
        self.appDBSession = None

    # Convenience
    def register_ash(self):
        self.userDB.registerUser("AshKetchum", "pallettown123", "000000000000", self.appDB)
    def register_misty(self):
        self.userDB.registerUser("Misty", "cerulean456", "111111111111", self.appDB)
    def ash_user(self):
        return self.appDBSession.things[0]
    def misty_user(self):
        return self.appDBSession.things[1]

    # Registration
    def test_registration(self):
        user = self.ash_user()
        self.assertEqual(user.username, "AshKetchum")
        self.assertTrue(self.appDB.session.didCommit)

    # Catching / Releasing
    def test_catching_pokemon_works(self):
        user = self.ash_user()
        # Catch Pikachu
        self.userDB.catchPokemonForUser(user, 25, self.appDB)
        # Grab the state of the Pokemon @ 25
        state = self.userDB._stateOfPokemonForUser(user, 25, self.appDB)
        state = int(state)
        self.assertEqual(state, 1)
    def test_new_user_hasnt_caught_pokemon(self):
        user = self.ash_user()
        # Grab the state of the Pokemon @ 25
        # It should be 0
        state = self.userDB._stateOfPokemonForUser(user, 25, self.appDB)
        state = int(state)
        self.assertEqual(state, 0)
    def test_catching_then_releasing_pokemon_works(self):
        user = self.ash_user()
        # Catch Pikachu
        self.userDB.catchPokemonForUser(user, 25, self.appDB)
        # Release Pikachu :-(
        self.userDB.uncatchPokemonForUser(user, 25, self.appDB)
        # Grab the state of the Pokemon @ 25
        state = self.userDB._stateOfPokemonForUser(user, 25, self.appDB)
        state = int(state)
        self.assertEqual(state, 0)

    # Comparison
    def test_comparing_user_without_pokemon_and_user_without_pokemon_returns_neither_having_pokemon(self):
        ash = self.ash_user()
        misty = self.misty_user()
        compared = self.userDB.comparedDexBetweenUsers(ash, misty, 1000)
        # Sigh... 24 is Pikachu (because index 0 is Pokemon #1, Bulbasaur)
        state_of_pikachu = int(compared[24])
        self.assertEqual(state_of_pikachu, 0)
    def test_comparing_user_with_pokemon_and_user_without_pokemon_returns_first_having_pokemon(self):
        ash = self.ash_user()
        misty = self.misty_user()
        self.userDB.catchPokemonForUser(ash, 25, self.appDB)
        compared = self.userDB.comparedDexBetweenUsers(ash, misty, 1000)
        state_of_pikachu = int(compared[24])
        self.assertEqual(state_of_pikachu, 1)
    def test_comparing_user_without_pokemon_and_user_with_pokemon_returns_second_having_pokemon(self):
        ash = self.ash_user()
        misty = self.misty_user()
        self.userDB.catchPokemonForUser(misty, 116, self.appDB)
        compared = self.userDB.comparedDexBetweenUsers(ash, misty, 1000)
        # 115 is Horsea (#116)
        state_of_horsea = int(compared[115])
        self.assertEqual(state_of_horsea, 2)
    def test_comparing_user_with_pokemon_and_user_with_pokemon_returns_both_having_pokemon(self):
        ash = self.ash_user()
        misty = self.misty_user()
        self.userDB.catchPokemonForUser(ash, 128, self.appDB)
        self.userDB.catchPokemonForUser(misty, 128, self.appDB)
        compared = self.userDB.comparedDexBetweenUsers(ash, misty, 1000)
        # 127 is Tauros (#128)
        state_of_tauros = int(compared[127])
        self.assertEqual(state_of_tauros, 3)

if __name__ == '__main__':
    unittest.main()
