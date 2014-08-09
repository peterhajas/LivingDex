class NationalDex:
    def __init__(self, pathToNationalDex):
        self.pokemon = {}

        with open(pathToNationalDex, 'r') as nationalDexFile:
            for line in nationalDexFile:
                pokedexNumber = line.split(' ')[0]
                self.pokemon[pokedexNumber] = line[len(pokedexNumber)+1:-1]
        self.numberOfPokemon = len(self.pokemon.keys())
    def pokemonNameForNumber(self, number):
        return self.pokemon[number]

