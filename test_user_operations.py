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
    def tearDown(self):
        self.userDB = None
        self.appDB = None
        self.appDBSession = None
    def register_ash(self):
        self.userDB.registerUser("AshKetchum", "pallettown123", "000000000000", self.appDB)

    def test_registration(self):
        self.register_ash()
        user = self.appDBSession.things[0]
        self.assertEqual(user.username, "AshKetchum")
        self.assertTrue(self.appDB.session.didCommit)
    def test_catching_pokemon_works(self):
        self.register_ash()
        user = self.appDBSession.things[0]
        # Catch Pikachu
        self.userDB.catchPokemonForUser(user, 25, self.appDB)
        # Grab the state of the Pokemon @ 25
        state = self.userDB._stateOfPokemonForUser(user, 25, self.appDB)
        state = int(state)
        self.assertEqual(state, 1)
    def test_new_user_hasnt_caught_pokemon(self):
        self.register_ash()
        user = self.appDBSession.things[0]
        # Grab the state of the Pokemon @ 25
        # It should be 0
        state = self.userDB._stateOfPokemonForUser(user, 25, self.appDB)
        state = int(state)
        self.assertEqual(state, 0)
    def test_catching_then_releasing_pokemon_works(self):
        self.register_ash()
        user = self.appDBSession.things[0]
        # Catch Pikachu
        self.userDB.catchPokemonForUser(user, 25, self.appDB)
        # Release Pikachu :-(
        self.userDB.uncatchPokemonForUser(user, 25, self.appDB)
        # Grab the state of the Pokemon @ 25
        state = self.userDB._stateOfPokemonForUser(user, 25, self.appDB)
        state = int(state)
        self.assertEqual(state, 0)


if __name__ == '__main__':
    unittest.main()
