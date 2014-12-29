import json
from collections import defaultdict

class NationalDex:
    def __init__(self, pathToNationalDex):
        dexfile = open(pathToNationalDex, 'r')
        self.dexdata = json.load(dexfile)
        self.numberOfPokemon = len(self.dexdata.keys())
        self.pokemonNames = []
        self.pokemonSlugs = []
        self.pokemonForms = defaultdict(list)

        for i in range (1, self.numberOfPokemon+1):
            dexKey = str(i).zfill(3)
            name = self.dexdata[dexKey]['name']['eng']
            slug = self.dexdata[dexKey]['slug']['eng']
            forms = self.dexdata[dexKey]['icons']

            self.pokemonNames.append(name)
            self.pokemonSlugs.append(slug)
            
            for form in forms:
                if form == '.':
                    if 'has_female' in forms['.'].keys():
                        self.pokemonForms[dexKey].append('female')
                    continue
                self.pokemonForms[dexKey].append(form)
