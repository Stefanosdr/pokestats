from pokemon_types import POKEMON_TYPE_NAMES
from itertools import combinations

class PokemonTriad():

    def __init__(self, pokemon_triad):
        self.cannot_cover = []
        self.can_cover = []
        self.pokemon_triad = pokemon_triad
        self.pokemon_triads = []
        self.times_weak_against_type = {pokemon_type: 0 for pokemon_type in POKEMON_TYPE_NAMES}
        self.times_resistant_against_type = {pokemon_type: 0 for pokemon_type in POKEMON_TYPE_NAMES}
        self.get_types_can_be_covered()

    def get_types_can_be_covered(self):
        for pokemon in self.pokemon_triad:
            for pokemon_type in POKEMON_TYPE_NAMES:
                if pokemon.damage_per_type2[pokemon_type] < 1:
                    self.times_resistant_against_type[pokemon_type] += 1
                    if pokemon_type not in self.can_cover:
                        self.can_cover.append(pokemon_type)
                else:
                    self.times_weak_against_type[pokemon_type] += 1
                    if pokemon_type not in self.cannot_cover:
                        self.cannot_cover.append(pokemon_type)


