import json

class NationalDex:
    def __init__(self, pathToNationalDex):
        dexfile = open(pathToNationalDex, 'r')
        self.dexdata = json.load(dexfile)
        self.numberOfPokemon = len(self.dexdata.keys())
        self.pokemonNames = []
        self.pokemonSlugs = []

        for i in range (1, self.numberOfPokemon+1):
            dexKey = str(i).zfill(3)
            name = self.dexdata[dexKey]['name']['eng']
            slug = self.dexdata[dexKey]['slug']['eng']
            self.pokemonNames.append(name)
            self.pokemonSlugs.append(slug)

    def pokemonNameForNumber(self, number):
        return self.pokemon[number]

