import json
import re

def json_naar_dict():
    global steamdata
    # json file openen
    with open('steam.json') as json_file:
        #json naar lijst
        steamdata = json.load(json_file)
        # #lijst naar dict
        # steamdata = new_dict = dict((item['appid'], item) for item in steamdata_list)
        return steamdata


def sorteren():
    global gesorteerd
    json_naar_dict()
    # laat de gebruiker kiezen waar hij op sorteerd
    categorie_input = input('1=naam\n2=release_date\n3=price\nwaar wil je op sorteren: ')
    if categorie_input == '1':
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
                # print(i)
                names.append(i)
        names.sort()
        gesorteerd = names
        return gesorteerd
    elif categorie_input == '2':
        #sorteer op de release date
        gesorteerd = sorted(steamdata, key=lambda k: k['release_date'], reverse=False)
        return gesorteerd
    elif categorie_input == '3':
        # sorteer op de prijs
        gesorteerd = sorted(steamdata, key=lambda k: k['price'], reverse=False)
        return gesorteerd


def naam_eerste_spel():
    json_naar_dict()
    sorteren()
    # check welk type de variable gesorteerd is om te bepalen hoe je de naam moet returnen
    # als je op naam sorteerd krijg je een lijst namen en is de eerste naam een string
    # als je op andere dingen sorteerd krijg je een lijst met dict's dus moet je nu specificeren dat je op 'name'zoekt
    if type(gesorteerd[0]) is str:
        eerste_spel = gesorteerd[0]
        return eerste_spel
    else:
        eerste_spel = gesorteerd[0]
        return eerste_spel['name']

print(naam_eerste_spel())
