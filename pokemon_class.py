import requests
from pokemon_types import POKEMON_TYPE_NAMES
import pandas as pd
from bs4 import BeautifulSoup as bs


ENDPOINT = "https://pokeapi.co/api/v2/pokemon/"

class Pokemon:
    def __init__(self, pokemon_name):
        self.name = pokemon_name
        self.response = requests.get(url=ENDPOINT + self.name.lower())
        self.response.raise_for_status()
        self.data = self.response.json()
        self.get_abilities()
        self.get_stats()
        self.get_egg_groups()
        self.get_types()
        self.get_pkmn_image_url()
        self.get_resistances_easier()
        self.num_neutral_res = 0
        self.num_half_damage_res = 0
        self.num_one_fourth_damage_res = 0
        self.num_immune = 0
        self.num_double_damage_res = 0
        self.num_quadraple_damage_res = 0
        self.get_num_resistances()


        #self.get_no_damage_from()
        #self.get_half_damage_from()
        self.get_abilities()
        #self.show_resistances()


    def get_abilities(self):
        self.abilities = []
        for ab in self.data.get("abilities"):
            ability = dict()
            ability["name"] = ab.get("ability").get("name")
            ability_response = requests.get(url=ab.get("ability").get("url"))
            ability_response.raise_for_status()
            ab_data = ability_response.json()
            for entry in ab_data.get("effect_entries"):
                if entry.get("language").get("name") == "en":
                    ability["description"] = entry.get("effect")
                    break
            self.abilities.append(ability)

    def get_stats(self):
        self.stats = []
        for st in self.data.get("stats"):
            stat = dict()
            stat["name"] = st.get("stat").get("name")
            stat["base_stat"] = st.get("base_stat")
            self.stats.append(stat)

    def get_types(self):
        self.types = []
        for pkmn_type in self.data.get("types"):
            type_dict = dict()
            type_dict["name"] = pkmn_type.get("type").get("name")
            type_dict["url"] = pkmn_type.get("type").get("url")
            #print(type_dict)
            self.types.append(type_dict)
        #print(self.types)



    def get_resistances_easier(self):
        self.damage_per_type2 = {type_name: 1 for type_name in POKEMON_TYPE_NAMES}
        damage_categories = dict()

        def get_damage_per_type(pokemon_type):
            if pokemon_type in damage_categories["category"]["list_of_types"]:
                self.damage_per_type2[pokemon_type] *= damage_categories["category"]["multiplier"]

        type_1_no_damage = [pkmn_type.get("name") for pkmn_type in
                            requests.get(self.types[0].get("url")).json().get("damage_relations").get(
                                "no_damage_from")]
        damage_categories["type1_no_damage"] = {"list_of_types": type_1_no_damage, "multiplier": 0}
        type_1_half_damage_from = [pkmn_type.get("name") for pkmn_type in
                                   requests.get(self.types[0].get("url")).json().get("damage_relations").get(
                                       "half_damage_from")]
        damage_categories["type1_half_damage"] = {"list_of_types": type_1_half_damage_from, "multiplier": 0.5}
        type_1_double_damage_from = [pkmn_type.get("name") for pkmn_type in
                                     requests.get(self.types[0].get("url")).json().get("damage_relations").get(
                                         "double_damage_from")]
        damage_categories["type1_double_damage"] = {"list_of_types": type_1_double_damage_from, "multiplier": 2}

        if len(self.types) > 1:
            type_2_no_damage = [pkmn_type.get("name") for pkmn_type in
                                   requests.get(self.types[1].get("url")).json().get("damage_relations").get(
                                       "no_damage_from")]
            damage_categories["type2_no_damage"] = {"list_of_types": type_2_no_damage, "multiplier": 0}
            type_2_half_damage_from = [pkmn_type.get("name") for pkmn_type in
                                        requests.get(self.types[1].get("url")).json().get("damage_relations").get(
                                       "half_damage_from")]
            damage_categories["type2_half_damage"] = {"list_of_types": type_2_half_damage_from, "multiplier": 0.5}
            type_2_double_damage_from = [pkmn_type.get("name") for pkmn_type in
                                         requests.get(self.types[1].get("url")).json().get("damage_relations").get(
                                             "double_damage_from")]
            damage_categories["type2_double_damage"] = {"list_of_types": type_2_double_damage_from, "multiplier": 2}

        for pokemon_type in POKEMON_TYPE_NAMES:
            for key, value in damage_categories.items():
                if pokemon_type in value.get("list_of_types"):
                    self.damage_per_type2[pokemon_type] *= value.get("multiplier")


    def get_num_resistances(self):
        for pkmn_type in self.damage_per_type2:
            if self.damage_per_type2.get(pkmn_type) == 0:
                self.num_immune += 1
            elif self.damage_per_type2.get(pkmn_type) == 1:
                self.num_neutral_res += 1
            elif self.damage_per_type2.get(pkmn_type) == 2:
                self.num_double_damage_res += 1
            elif self.damage_per_type2.get(pkmn_type) == 4:
                self.num_quadraple_damage_res += 1
            elif self.damage_per_type2.get(pkmn_type) == 0.25:
                self.num_one_fourth_damage_res += 1
            else:
                self.num_half_damage_res += 1



    def get_egg_groups(self):
        self.egg_groups = []
        egg_moves_end_point = f"https://www.serebii.net/pokedex-swsh/{self.name.lower()}/egg.shtml"
        egg_moves_df = pd.read_html(egg_moves_end_point)[4]
        if not pd.isna(egg_moves_df.iloc[1, 3]):
            self.egg_groups.append(egg_moves_df.iloc[1][3])
        if not pd.isna(egg_moves_df.iloc[1, 4]):
            self.egg_groups.append(egg_moves_df.iloc[1][4])

    def get_pkmn_image_url(self):
        url = f"https://www.serebii.net/pokedex-swsh/{self.name.lower()}"
        response = requests.get(url=url)
        response.raise_for_status()
        page = response.text
        soup = bs(page, "lxml")
        pkmn_image = soup.find_all("img", alt="Normal Sprite")
        self.image_url = f"https://serebii.net{pkmn_image[0]['src']}"



    def get_egg_moves(self):
        pass

    #TODO find all moves that can be learned via breeding
    #TODO list all available pokemon that can pass down these moves via breeding

