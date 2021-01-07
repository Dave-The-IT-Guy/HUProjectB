import json
import re

def json_to_dict():
    #Open de json file en zet alle in een dictonairy
    with open('steam.json') as json_file:
        steamdata = json.load(json_file)
    return steamdata


def clean():
    steamdata = json_to_dict()
    # Maak een lege lijst aan voor de namen
    names = []
    # Loop door de dictionaries in de lijst
    for i in steamdata:
        # Haal de waarde van de name key uit de dict
        i = i['name']
        # Maak er een string van
        i = str(i)
        # Haal met regex de meeste speciale karakters eruit
        i = re.sub(r'\W+', '', i)  # [^A-Za-z0-9]
        # Als de string niet false is voeg hem toe aan de lijst (strings kunnen false zijn als ze bijv. leeg zijn)
        if i:
            names.append(i)
    return names

def sort():
    pass

def name_first_game():
    json_to_dict()
    clean()
    # check welk type de variable gesorteerd is om te bepalen hoe je de naam moet returnen
    # als je op naam sorteerd krijg je een lijst namen en is de eerste naam een string
    # als je op andere dingen sorteerd krijg je een lijst met dict's dus moet je nu specificeren dat je op 'name'zoekt
    if type(sort[0]) is str:
        first_game = sort[0]
        return first_game
    else:
        first_game = sort[0]
        return first_game['name']

print(name_first_game())
