import json

class NationalDex:
    def __init__(self, pathToNationalDex):
        dexfile = open(pathToNationalDex, 'r')
        self.dexdata = json.load(dexfile)
        self.numberOfPokemon = len(self.dexdata.keys())
        self.pokemonNames = []

        for i in range (1, self.numberOfPokemon):
            dexKey = str(i).zfill(3)
            name = self.dexdata[dexKey]['name']['eng']
            self.pokemonNames.append(name)

    def pokemonNameForNumber(self, number):
        return self.pokemon[number]

