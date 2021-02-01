from pokemon_team import PokemonTriad
from itertools import combinations
from pokemon_class import Pokemon

def get_pokemon_triads(pokemon_list):
    pokemon_objects = [Pokemon(pokemon_name) for pokemon_name in pokemon_list]
    pokemon_triads = [PokemonTriad(pokemon_triad) for pokemon_triad in list(combinations(pokemon_objects, 3))]
    return pokemon_triads

'''
pokemon_names = ["Gardevoir", "Blastoise", "Golduck", "Venusaur", "Raichu", "Flygon"]
pokemon_objects = [Pokemon(pokemon_name) for pokemon_name in pokemon_names]

triads = get_pokemon_triads(pokemon_objects)
for triad in triads:
    print(triad.times_resistant_against_type)
'''