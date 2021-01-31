import requests

POKEMON_TYPES = [pokemon_type for pokemon_type in
                 requests.get(url="https://pokeapi.co/api/v2/type/").json().get("results")
                 if pokemon_type.get("name") != "unknown" and pokemon_type.get("name") != "shadow"]

POKEMON_TYPE_NAMES = [pokemon_type.get("name") for pokemon_type in POKEMON_TYPES]
print(len(POKEMON_TYPE_NAMES))