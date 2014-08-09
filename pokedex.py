class NationalDex:
    def __init__(self, pathToNationalDex):
        self.pokemon = {}
        self.pokemonNames = [ ]

        with open(pathToNationalDex, 'r') as nationalDexFile:
            for line in nationalDexFile:
                pokedexNumber = line.split(' ')[0]
                pokemonName = line[len(pokedexNumber)+1:-1]
                self.pokemon[pokedexNumber] = pokemonName
                self.pokemonNames.append(pokemonName)

        self.numberOfPokemon = len(self.pokemon.keys())
    def pokemonNameForNumber(self, number):
        return self.pokemon[number]

