# Please note that this is not writen by a professional python developper and an english speaker
# Hope it's not like acid in the eyes for professionnal developpers :)
# Don't forget to change the dictionaries and the names of the files (or path) you'll use
import re
from pathlib import Path
import json
import os

NUM_POKEDEX_FIRST_MINUS_ONE = 809
GENDER_CORR = {"FemaleOneEighth":12.5, "Female50Percent":50, "Female75Percent":75, "Female25Percent":25, "FemaleSevenEighths":87.5, "Genderless":-1, "AlwaysFemale":100, "AlwaysMale":0}
EXP_CORR = {"Parabolic":2, "Slow":3, "Medium":1, "Erratic":4, "Fast":0, "Fluctuating":5}
EV_CORR = {"SPECIAL_ATTACK":"Ats", "ATTACK":"Atk", "HP":"Hp", "SPEED":"Spd", "DEFENSE":"Dfe", "SPECIAL_DEFENSE":"Dfs"}
BREED_GROUPS_CORR = {"Monster":1, "Water1":2, "Bug":3, "Flying":4, "Field":5,  "Fairy":6, "Grass":7, "Humanlike":8,  "Water3":9,  "Mineral":10, "Amorphous":11, "Water2":12,  "Ditto":13, "Dragon":14, "Undiscovered":15}
EVOLUTIONS_SPE = {"Item":"stone", "Level":"minLevel", "Trade":"trade", "LevelRain":["minLevel","rain"], "HasMove":"skill1", "HoldItem":"itemHold", "Event":"minLevel", "HappinessNight":[{"type": "minLoyalty","value": 220},{"type": "dayNight","value": 0}]}

def rename_graphics (pok_name, src_folder, dest_folder, extension=".png"):
    """Helps to rename and copy all of the assests (taken from essentials) from POKEMONNAME_FORMBUMBER.png
    (or .ogg) to POKEDEXNUMBER_FORMNUMBER.png (or .ogg)

    Args:
        pok_name (str): the pokemon's name (in CAPS)
        src_folder (str): the source's folder
        dest_folder (str): the destination's folder of the copy
        extension (str, optional): _description_. Defaults to ".png".
    """
    try:
        files = os.listdir(src_folder)
        matching_files = [
            file for file in files
            if file.startswith(pok_name) and file.endswith(extension)
        ]
        matching_files.sort()

        # Rename and copy the files
        for i, file in enumerate(matching_files):
            suffix = f"_{i}" if i > 0 else ""  # Add i for pokemons that have different forms
            new_name = f"{POKEDEX[pok_name]}{suffix}{extension}"

            old_path = os.path.join(src_folder, file)
            new_path = os.path.join(dest_folder, new_name)

            # Rename the files
            os.rename(old_path, new_path)
            print(f"Renommé : {old_path} → {new_path}")

    except Exception as e:
        print(f"Erreur : {e}")

def search_name_move(mov):
    """ Search the move like writen in Essentilas (ALLINCAPSWITHOUTSPACES) to the move writen in all_min_with_space
    Note: the ' is replaced by a _

    Args:
        mov (str): the move's name in Essentials

    Returns:
        str: the move's name in PSDK
    """
    try:
        with open("moves.txt", 'r', encoding="utf-8") as mf:
            lines = mf.readlines()
        for line in lines:
            line_clean = line.replace(' ','')
            line_clean = line_clean.replace('-','')
            line_clean = line_clean.lower()
            line_clean = line_clean.strip()
            if mov.lower().strip() == line_clean:
                name = line.replace(' ','_')
                name = name.replace('-','_')
                name = name.lower()
                return name.strip()

    except Exception as e:
        print(f"Erreur search_name_move: {e}")

def search_name_ability(ability):
    """ Search the ability like writen in Essentilas (ALLINCAPSWITHOUTSPACES) to the ability writen in all_min_with_spaces
    Note: the ' is replaced by a _

    Args:
        ability (str): the ability's name in Essentials

    Returns:
        str: the ability's name in PSDK
    """
    try:
        with open("abilities.txt", 'r', encoding="utf-8") as mf:
            lines = mf.readlines()
        for line in lines:
            line_clean = line.replace(' ','')
            line_clean = line_clean.replace('-','')
            line_clean = line_clean.replace("'",'')
            line_clean = line_clean.lower()
            line_clean = line_clean.strip()
            if ability.lower().strip() == line_clean:
                name = line.replace(' ','_')
                name = name.replace('-','_')
                name = name.replace("'", "_")
                name = name.lower()
                return name.strip()

    except Exception as e:
        print(f"Erreur search_name_move: {e}")

def search_name_obj(item):
    """ Search the item like writen in Essentilas (ALLINCAPSWITHOUTSPACES) to the move writen in all_min_with_space
    Note: the ' is replaced by a _

    Args:
        item (str): the item's name in Essentials

    Returns:
        str: the item's name in PSDK
    """
    try:
        with open("items.txt", 'r', encoding="utf-8") as mf:
            lines = mf.readlines()
        for line in lines:
            line_clean = line.replace(' ','')
            line_clean = line_clean.replace('-','')
            line_clean = line_clean.lower()
            line_clean = line_clean.strip()
            if item.lower().strip() == line_clean:
                name = line.replace(' ','_')
                name = name.replace('-','_')
                name = name.lower()
                return name.strip()

    except Exception as e:
        print(f"Erreur search_name_move: {e}")

def clean_name(str_name):
    """ Clean a string, used here for pokemon's name (but work for other things too)

    Args:
        str_name (str): pokemon's name to clean

    Returns:
        str: the pokemon's name clean (as in PSDK)
    """
    clean_str_name = str_name.replace(".","")
    clean_str_name = clean_str_name.replace(" ","_")
    clean_str_name = clean_str_name.replace("'","_")
    return clean_str_name

def txt_to_json(path_poke, num_pokedex):
    """Parse a pokemon's txt file and find SOME of the correct data needed for a
    pokemon's JSON file
    Note : all exceptions are not taking care of, they may be easier to treat by hand

    Args:
        path_poke (str): the path to the txt file
        num_pokedex (int): the pokemon's pokedex number
    """
    try:
        with open(path_poke, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # The classical format of json file
        json_data = {
            "klass": "Specie",
            "id": num_pokedex,
            "dbSymbol": None,
            "forms": [
                {
                    "form":0,
                    "formTextId":{
                        "name": num_pokedex+283,
                        "description": 0
                    },
                    "height":1,
                    "weight":1,
                    "type1": "__undef__",
                    "type2": "__undef__",
                    "baseHp": 100,
                    "baseAtk": 100,
                    "baseDfe": 100,
                    "baseSpd": 100,
                    "baseAts": 100,
                    "baseDfs": 100,
                    "evHp": 0,
                    "evAtk": 0,
                    "evDfe": 0,
                    "evSpd": 0,
                    "evAts": 0,
                    "evDfs": 0,
                    "evolutions": [],
                    "experienceType": 3,
                    "baseExperience": 230,
                    "baseLoyalty": 70,
                    "catchRate": 45,
                    "femaleRate": 50,
                    "breedGroups": [],
                    "hatchSteps": 5120,
                    "babyDbSymbol": "",
                    "babyForm": 0,
                    "itemHeld": [],
                    "abilities": [],
                    "frontOffsetY": 0,
                    "resources": {
                        "icon": "",
                        "iconShiny": "",
                        "front": "",
                        "frontShiny": "",
                        "back": "",
                        "backShiny": "",
                        "footprint": "",
                        "character": "",
                        "characterShiny": "",
                        "cry": "",
                        "hasFemale": False
                    },
                    "moveSet":[]
                }
            ]
        }
        
        # From there, it's no longer possible to know for sure at which line the informations will be (thanks to hidden abilities)

        # Loop through the last lines
        for i, line in enumerate(lines):
            # add the pokemon's name
            name_match = re.search(r"Name = (.+)", lines[1])
            if name_match:
                name_cleaned = clean_name(name_match.group(1).lower())
                json_data["dbSymbol"] = name_cleaned
            
            # add the pokemon's types
            type_match = re.search(r"Types = (\S*)", line)
            if type_match:
                types = type_match.group(1).split(",")
                json_data["forms"][0]["type1"] = types[0].lower()
                # Change the second type if existent
                if len(types)==2:
                    json_data["forms"][0]["type2"] = types[1].lower()
            
            # add the pokemon's stats
            stats_match = re.search(r"BaseStats = (\S*)", line)
            if stats_match:
                stats = stats_match.group(1).split(",")
                json_data["forms"][0]["baseHp"] = int(stats[0])
                json_data["forms"][0]["baseAtk"] = int(stats[1])
                json_data["forms"][0]["baseDfe"] = int(stats[2])
                json_data["forms"][0]["baseSpd"] = int(stats[3])
                json_data["forms"][0]["baseAts"] = int(stats[4])
                json_data["forms"][0]["baseDfs"] = int(stats[5])
            
            # add the pokemon's experience gain curv (see EXP_CORR for the bridge between Essentials and PSDK)
            exp_typ_match = re.search(r"GrowthRate = (\S*)", line)
            if exp_typ_match :
                exp_typ = exp_typ_match.group(1).strip()
                json_data["forms"][0]["experienceType"] = EXP_CORR[exp_typ]
            
            # add the pokemon's gender ratio (see GENDER_CORR for the bridge between Essentials and PSDK)
            gender_ratio_match = re.search(r"GenderRatio = (\S*)", line)
            if gender_ratio_match :
                gender_ratio = gender_ratio_match.group(1).strip()
                json_data["forms"][0]["femaleRate"] = GENDER_CORR[gender_ratio]

            # add the pokemon's base exp given
            base_exp_match = re.search(r"BaseExp = (\S*)", line)
            if base_exp_match:
                json_data["forms"][0]["baseExperience"] = int(base_exp_match.group(1).strip())
            
            # add the pokemon's ev given (see EV_CORR for the bridge between Essentials and PSDK)
            base_ev_match = re.search(r"EVs = (\S*)", line)
            if base_ev_match:
                EVs = base_ev_match.group(1).split(",")
                for k in range(0, len(EVs), 2):
                    json_data["forms"][0][f"ev{EV_CORR[EVs[k]]}"] = int(EVs[k+1])
            
            # add the pokemon's catch rate
            catch_rate_match = re.search(r"CatchRate = (\S*)", line)
            if catch_rate_match:
                json_data["forms"][0]["catchRate"] = int(catch_rate_match.group(1).strip())
            
            # add the pokemon's base happiness
            happiness_match = re.search(r"Happiness = (\S*)", line)
            if happiness_match:
                json_data["forms"][0]["baseLoyalty"] = int(happiness_match.group(1).strip())
            
            match = re.match(r"Moves = (\S*)", line) # Match the moves learned by level
            match_breed = re.match(r"EggMoves = (\S*)", line) # Match the moves learned via breeding
            match_tm = re.match(r"TutorMoves = (\S*)", line) # Match the moves learned via TM and Move Tutor
            height_match = re.search(r"Height = (\S*)", line) # Match the height
            weight_match = re.search(r"Weight = (\S*)", line) # Match the wheight
            hatch_step_match = re.search(r"HatchSteps = (\S*)", line)
            wild_item_match = re.search(r"WildItemUncommon = (\S*)", line)
            egg_group_match = re.search(r"EggGroups = (\S*)", line)
            
            # Here, it was necessary to match hidden abililies and not hidden abilities whitin the same loop
            abilities_match = re.search(r"^Abilities = (\S*)", lines[i-1]) # Match the abilities (not hidden)
            hidden_abilities_match = re.search(r"HiddenAbilities = (\S*)", line) # Match the hidden abilities
            
            evolutions_match = re.search(r"Evolutions = (\S*)", line) # Match the evolution (hard to code)

            # Add the LevelLearnable moveset
            if match:
                klass = "LevelLearnableMove"
                objects = match.group(1).split(",")
                # Construire les éléments "like"
                for i in range(0, len(objects), 2):
                    mov_name = objects[i+1].strip()
                    mov_name_clean = search_name_move(mov_name)
                    mov_level = int(objects[i].strip())
                    json_data["forms"][0]["moveSet"].append({
                        "klass": klass,
                        "move": mov_name_clean,
                        "level": mov_level
                    })
            # Add the TutorLearnable moveset
            # Note : I'm note sure if breeding=tutorlearnablemove but from what I've seen, it's seems ok
            if match_breed:
                klass = "TutorLearnableMove"
                tutor_moves = match_breed.group(1).split(",")
                for tutor_move in tutor_moves:
                    json_data["forms"][0]["moveSet"].append({
                        "klass":klass,
                        "move": search_name_move(tutor_move)
                    })
            # Add the TechLearnable moveset
            if match_tm:
                klass = "TechLearnableMove"
                tm_moves = match_tm.group(1).split(",")
                for tm_move in tm_moves:
                    json_data["forms"][0]["moveSet"].append({
                        "klass": klass,
                        "move": search_name_move(tm_move)
                    })
            # Add the height and weight
            if height_match:
                json_data["forms"][0]["height"] = float(height_match.group(1))
            if weight_match:
                json_data["forms"][0]["weight"] = float(weight_match.group(1))
            
            # Add the abilities like (1st ability, 2nd ability, hidden ability)
            # If 1 ability (1st ability, 1st ability, hidden ability)
            # If 1 ability and no hidden one (1st ability, 1st ability, 1st ability)
            if abilities_match:
                abilities = abilities_match.group(1).split(",")
                json_data["forms"][0]["abilities"].append(search_name_ability(abilities[0]))
                if len(abilities)>1:
                    json_data["forms"][0]["abilities"].append(search_name_ability(abilities[1]))
                else:
                    json_data["forms"][0]["abilities"].append(search_name_ability(abilities[0]))
                if hidden_abilities_match:
                    hidden_abilities = hidden_abilities_match.group(1).strip()
                    json_data["forms"][0]["abilities"].append(search_name_ability(hidden_abilities))
                else:
                    json_data["forms"][0]["abilities"].append(search_name_ability(abilities[0]))
            
            # Add the evolutions
            # Important note: all methods of evolutions are not taken care of
            if evolutions_match:
                evolutions = evolutions_match.group(1).strip().split(",")
                for j in range(0, len(evolutions), 3):
                    value = evolutions[j+2]
                    if EVOLUTIONS_SPE[evolutions[j+1]] == "skill1":
                        value = search_name_move(value)
                    elif EVOLUTIONS_SPE[evolutions[j+1]] in ["stone", "itemHold"]:
                        value = search_name_obj(value)
                    elif EVOLUTIONS_SPE[evolutions[j+1]] == "minLevel":
                        value = int(value)
                    na_evo = ""
                    if evolutions[j+2]=="":
                        evolutions[j+2] = True
                    try:
                        with open(f"txt_8gen/{evolutions[j]}.txt", 'r', encoding='utf-8') as na:
                            na_lines = na.readlines()
                        na_evo_match = re.search(r"Name = (.+)", na_lines[1])
                        with open(f"txt_8gen/{evolutions[j].lower()}.txt", 'w', encoding='utf-8') as na_w:
                            na_w.write(f"{clean_name(name_match.group(1).lower())}")
                            print(f"Bébé ajouté dans {evolutions[j]}")
                        if na_evo_match:
                            na_evo = clean_name(na_evo_match.group(1).lower())
                    except Exception as e:
                        print(f"Erreur evolutions match : {e}")
                    if evolutions[j+1] in ["HappinessNight", "HappinessDay"]: # Add whatever you need
                        json_data["forms"][0]["evolutions"].append({
                            "dbSymbol": na_evo,
                            "form": 0,
                            "conditions": EVOLUTIONS_SPE[evolutions[j+1]],
                        })
                    else:
                        json_data["forms"][0]["evolutions"].append({
                            "dbSymbol": na_evo,
                            "form": 0,
                            "conditions":[
                                {
                                    "type": EVOLUTIONS_SPE[evolutions[j+1]],
                                    "value": value
                                }
                            ]
                        })

            if hatch_step_match:
                json_data["forms"][0]["hatchSteps"] = int(hatch_step_match.group(1))

            if wild_item_match :
                json_data["forms"][0]["itemHeld"].append({
                    "dbSymbol": search_name_obj(wild_item_match.group(1)),
                    "chance": 5
                })
            else: 
                json_data["forms"][0]["itemHeld"].append({
                    "dbSymbol": "none",
                    "chance": 0
                })
                json_data["forms"][0]["itemHeld"].append({
                    "dbSymbol": "none",
                    "chance": 0
                })
            if egg_group_match:
                for breed in egg_group_match.group(1).split(","):
                    if len(egg_group_match.group(1).split(","))==1:
                        json_data["forms"][0]["breedGroups"].append(BREED_GROUPS_CORR[breed])    
                    json_data["forms"][0]["breedGroups"].append(BREED_GROUPS_CORR[breed])
        
        json_data["forms"][0]["resources"]["icon"] = str(num_pokedex)
        json_data["forms"][0]["resources"]["front"] = str(num_pokedex)
        json_data["forms"][0]["resources"]["frontShiny"] = str(num_pokedex)
        json_data["forms"][0]["resources"]["back"] = str(num_pokedex)
        json_data["forms"][0]["resources"]["backShiny"] = str(num_pokedex)
        json_data["forms"][0]["resources"]["cry"] = str(num_pokedex)
        json_data["forms"][0]["resources"]["character"] = str(num_pokedex)
        #only works for 1 and 2 stages evolutions
        try:
            with open(path_poke.lower(), "r", encoding="utf-8") as bb:
                baby_name = bb.read()
            json_data["forms"][0]["babyDbSymbol"] = baby_name
        except:
            json_data["forms"][0]["babyDbSymbol"] = name_cleaned

                

        # Écriture dans le fichier JSON
        output_file = f"json_8gen/{clean_name(name_match.group(1).lower())}.json"

        with open(output_file, 'w', encoding='utf-8') as out_f:
            json.dump(json_data, out_f, indent=2)
        
        print(f"Fichier JSON écrit : {output_file}")

    except Exception as e:
        print(f"Erreur txt_to_json : {e}")

def separate_txt_file():
    """Split the big txt file containing all pokemons into indindual ones
    """
    gen8_txt_pathfile = Path("pokemon_8gen.txt")
    all_txt = ""
    if gen8_txt_pathfile.exists():
        try:
            with gen8_txt_pathfile.open("r", encoding="utf-8") as pok_text:
                all_txt = pok_text.read()
        except IOError:
            print(
                f"Couldn't retrieve data from file {gen8_txt_pathfile}, starting from scratch."
            )
    else:
        print("No data file found, starting from scratch.")
    separator_regex = re.compile(r"#-------------------------------")
    name_regex = re.compile(r"\[(.+)\]")
    sections = re.split(separator_regex, all_txt)
    for i, section in enumerate(sections):
        section = section.strip()
        if not section:
            continue
        match = re.search(name_regex, section)
        if match:
            name = match.group(1).strip()
            output_file = f"txt_8gen/{name}.txt"
            with open(output_file, 'w', encoding='utf-8') as out_f:
                out_f.write(section)# Écrire la section entière
                num_pokedex = NUM_POKEDEX_FIRST_MINUS_ONE+i
                out_f.write(f"\nNPOKEDEX = {num_pokedex}")
                print(f"Section sauvegardée dans {output_file}")
            txt_to_json(output_file, num_pokedex)
        else:
            print(f"Nom introuvable dans la section {i + 1}, section ignorée.")

# The pokemon's name like seen in Essentials as Key and the pokedex number as value
# You can update this dict to correspond to the pokemons you want to import from essentials
POKEDEX = {
    "POIPOLE": 803,
    "NAGANADEL": 804,
    "STAKATAKA":805,
    "BLACEPHALON": 806,
    "ZERAORA":807,
    "MELTAN":808,
    "MELMETAL":809,
    "GROOKEY": 810,
    "THWACKEY": 811,
    "RILLABOOM": 812,
    "SCORBUNNY": 813,
    "RABOOT": 814,
    "CINDERACE": 815,
    "SOBBLE": 816,
    "DRIZZILE": 817,
    "INTELEON": 818,
    "SKWOVET": 819,
    "GREEDENT": 820,
    "ROOKIDEE": 821,
    "CORVISQUIRE": 822,
    "CORVIKNIGHT": 823,
    "BLIPBUG": 824,
    "DOTTLER": 825,
    "ORBEETLE": 826,
    "NICKIT": 827,
    "THIEVUL": 828,
    "GOSSIFLEUR": 829,
    "ELDEGOSS": 830,
    "WOOLOO": 831,
    "DUBWOOL": 832,
    "CHEWTLE": 833,
    "DREDNAW": 834,
    "YAMPER": 835,
    "BOLTUND": 836,
    "ROLYCOLY": 837,
    "CARKOL": 838,
    "COALOSSAL": 839,
    "APPLIN": 840,
    "FLAPPLE": 841,
    "APPLETUN": 842,
    "SILICOBRA": 843,
    "SANDACONDA": 844,
    "CRAMORANT": 845,
    "ARROKUDA": 846,
    "BARRASKEWDA": 847,
    "TOXEL": 848,
    "TOXTRICITY": 849,
    "SIZZLIPEDE": 850,
    "CENTISKORCH": 851,
    "CLOBBOPUS": 852,
    "GRAPPLOCT": 853,
    "SINISTEA": 854,
    "POLTEAGEIST": 855,
    "HATENNA": 856,
    "HATTREM": 857,
    "HATTERENE": 858,
    "IMPIDIMP": 859,
    "MORGREM": 860,
    "GRIMMSNARL": 861,
    "OBSTAGOON": 862,
    "PERRSERKER": 863,
    "CURSOLA": 864,
    "SIRFETCHD": 865,
    "MRRIME": 866,
    "RUNERIGUS": 867,
    "MILCERY": 868,
    "ALCREMIE": 869,
    "FALINKS": 870,
    "PINCURCHIN": 871,
    "SNOM": 872,
    "FROSMOTH": 873,
    "STONJOURNER": 874,
    "EISCUE": 875,
    "INDEEDEE": 876,
    "MORPEKO": 877,
    "CUFANT": 878,
    "COPPERAJAH": 879,
    "DRACOZOLT": 880,
    "ARCTOZOLT": 881,
    "DRACOVISH": 882,
    "ARCTOVISH": 883,
    "DURALUDON": 884,
    "DREEPY": 885,
    "DRAKLOAK": 886,
    "DRAGAPULT": 887,
    "ZACIAN": 888,
    "ZAMAZENTA": 889,
    "ETERNATUS": 890,
    "KUBFU": 891,
    "URSHIFU": 892,
    "ZARUDE": 893,
    "REGIELEKI": 894,
    "REGIDRAGO": 895,
    "GLASTRIER": 896,
    "SPECTRIER": 897,
    "CALYREX": 898,
}

def main():
    separate_txt_file()
    
    # Si vous devez renommez les ressources
    # for pok in POKEDEX:
    #     rename_graphics(pok,"pokemon_essentials/Front","graphics/pokedex/pokefront")
    #     rename_graphics(pok,"pokemon_essentials/Back","graphics/pokedex/pokeback")
    #     rename_graphics(pok,"pokemon_essentials/Front shiny","graphics/pokedex/pokefrontshiny")
    #     rename_graphics(pok,"pokemon_essentials/Back shiny","graphics/pokedex/pokebackshiny")
    #     rename_graphics(pok,"pokemon_essentials/Icons","graphics/pokedex/pokeicon")
    #     rename_graphics(pok,"pokemon_essentials/Cries","audio/se/cries", ".ogg")

if __name__ == "__main__":
    main()
