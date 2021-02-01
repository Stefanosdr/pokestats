from pokemon_team import PokemonTriad
from itertools import combinations
from pokemon_class import Pokemon
import concurrent.futures


def get_pokemon_triads(pokemon_list):
    def create_pokemon_object(pokemon_name):
        try:
            pokemon_object = Pokemon(pokemon_name)
        except Exception as err:
            print(f"Error while retrieving data for {pokemon_name}")
        return pokemon_object
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(create_pokemon_object, pokemon_list)
        print(results)
    #pokemon_objects = [Pokemon(pokemon_name) for pokemon_name in pokemon_list]
        pokemon_triads = [PokemonTriad(pokemon_triad) for pokemon_triad in list(combinations(results, 3))]
        return pokemon_triads

'''
pokemon_names = ["Gardevoir", "Blastoise", "Golduck", "Venusaur", "Raichu", "Flygon"]
pokemon_objects = [Pokemon(pokemon_name) for pokemon_name in pokemon_names]

triads = get_pokemon_triads(pokemon_objects)
for triad in triads:
    print(triad.times_resistant_against_type)
'''