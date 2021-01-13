# steam project dashboard - verona kragten

#TODO: Deze regel overal aanpassen sorted_dict = sorted(json_to_dict(data_location), key=lambda k: k['price'])  # sort list of dicts

from tkinter import *
import webbrowser
import json
import re
from tkinter import ttk
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkcolorpicker import askcolor
import threading
import Pyro5.api
import time
from tkinter import tix
from tkinter.constants import *
from PIL import ImageTk,Image
import requests
import pandas as pd



# -- globals
global case_sensitive
case_sensitive = True
global sorting
global games_from_list
global sensordisplay
sensordisplay = "neopixel"
#Voor de verbinding met de server
con = "PYRO:steam.functions@192.168.192.24:9090"
#Locatie van steam.json voor als de API niet werkt
data_location = "steam.json"

# -- to do
# make graph blue
# repair getdetails function
# put more graphs in graphframe
# fix neopixel button
# the sort functions give differing lists containing games that dont appear in the original list

# neopxel functies
# zwaaiknop servo *
# afstandsensor toggle*
# hoeveel vrienden online (hoeft niet in gui)
# color picker geef alleen rgb waarden teruggeven*
# knop voor geluidsignaal*

# beginnen met functies
# met pyro commands sturen naar rpi

# -- functions
def openReadme():
    webbrowser.open('https://github.com/Dave-The-IT-Guy/HUProjectB/blob/main/README.md')

def listInsert(list):
    for item in list:
        gameslist.insert(END, item)

###############################################################
###############SINDS GEBRUIK API NIET MEER NODIG###############
###############################################################
def json_to_dict(location):
    #Open de json file en zet alles in een dictonairy
    with open(location) as json_file:
        steamdata = json.load(json_file)
    return steamdata

def select(dict, selection):
    # Maak een lege lijst aan voor de namen
    result = []
    # Loop door de dictionaries in de lijst
    for i in dict:
        # Haal de waarde van de name key uit de dict
        i = i[selection]
        # Maak er een string van
        i = str(i)
        # Haal met regex de meeste speciale karakters eruit
        i = re.sub('[^A-Za-z0-9$()\&\+\'\:\w\-\s\.]+', '', i)  # [^A-Za-z0-9]

        # Haal alle onnodige spaties weg
        i = " ".join(i.split())
        # Haal wat extra rotzooi uit de string
        (i).replace('()', '')
        i.strip()

        # Als een string met ' begint en eindigd verwijder deze dan
        if i.startswith('\'') == True and i.endswith('\'') == True:
            i = i[1:(len(i) - 1)]

        # Als de string niet false is voeg hem toe aan de lijst (strings kunnen false zijn als ze bijv. leeg zijn)
        if i:
            result.append(i)
    return result

###############################################################################################################################################################

#Source: https://www.geeksforgeeks.org/merge-sort/
def sort(lst):

    if len(lst) > 1:

        # Vind het midden van de lijst
        center = len(lst) // 2

        # Bepaal de linkerkant van de lijst
        left = lst[:center]

        # Bepaal de rechterkant van de lijst
        right = lst[center:]

        # Sorteerd de eerste helft van de lijst
        sort(left)

        # Sorteerd de tweede helft van de lijst
        sort(right)

        # Variabelen die gebruit worden om te tellen
        i = j = k = 0

        # Kopieeert de data in 2 tijdelijke lijsten
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                lst[k] = left[i]
                i += 1
            else:
                lst[k] = right[j]
                j += 1
            k += 1

        # Checkt voor overgebleven elementen als die er zijn (links)
        while i < len(left):
            lst[k] = left[i]
            i += 1
            k += 1

        # Checkt voor overgebleven elementen als die er zijn (rechts)
        while j < len(right):
            lst[k] = right[j]
            j += 1
            k += 1
    return lst

###############################################################
###############SINDS GEBRUIK API NIET MEER NODIG###############
###############################################################
def sort_json(location, sort_by):
    # Maak van de json een dict
    dict = json_to_dict(location)

    # Maakt een lijst van alle data die bij de gekozen sleutel hoort
    lst = select(dict, sort_by)

    # Returnt een gesorteerde variant van de lijst
    return sort(lst)

###############################################################################################################################################################

def get_request(url, parameters=None):

    try:
        response = requests.get(url=url, params=parameters)
    except:
        time.sleep(2)
        # recusively try again
        return get_request(url, parameters)

    if response:
        return response.json()
    else:
        # response is none usually means too many requests. Wait and try again
        time.sleep(2)
        return get_request(url, parameters)


def collectInfo(**kwargs):

    game = kwargs.get('gameID', None)

    if game == None or game == "all":
        url = "https://steamspy.com/api.php?request=all"
    else:
        url = "https://steamspy.com/api.php?request=appdetails&appid=" + str(game)

    # request 'all' from steam spy and parse into dataframe
    json_data = get_request(url)

    if game == None or game == "all":
        json_data = pd.DataFrame.from_dict(json_data, orient='index')

    return (json_data)


def showgraph(appID, *rating):
    if appID != 0:
        app = collectInfo(gameID = appID)

        positive = app['positive']
        negative = app['negative']
        sizes = [positive, negative]
    #Als de api niet werkt kan er op deze manier toch een grafiek getoont worden
    else:
        sizes = rating[0]

    ax1.clear()
    ax1.pie(sizes, explode=[0.1, 0], labels=["Positief", "Negatief"], autopct='%1.0f%%', shadow=True, startangle=45)
    fig1.canvas.draw_idle()

###############################################################################################################################################################
###############################################################################################################################################################
###############################################################################################################################################################

def showPlaytime():
    t = [1, 2, 3, 4, 5, 6]
    s = [1, 2, 3, 4, 5, 6]
    fig, ax = plt.subplots(facecolor="#042430")
    # fig.set_size_inches(2.5, 2.5)
    ax.set_facecolor('#0B3545')
    ax.set_title('playtime', color='white')
    ax.set_xlabel('time (s)', color='white')
    ax.set_ylabel('playtime', color='white')
    ax.plot(t, s, 'xkcd:red')
    ax.plot(t, s, color='white', linestyle='--')
    ax.tick_params(labelcolor='white')

    canvas1 = FigureCanvasTkAgg(fig, master=ntbk_frame1,)
    canvas1.draw()

    toolbar = NavigationToolbar2Tk(canvas1, ntbk_frame1)
    toolbar.update()

    canvas1.get_tk_widget().pack()


def fillList(fill_with):
    try:
        games = collectInfo()
        list = games[fill_with].to_list()
    except:
        list = []
        for game in json_to_dict(data_location):
            list.append(game[fill_with])
    return list


def getDetails(i):
    selected = gameslist.get(gameslist.curselection()) # get the current selection in the listbox
    details.config(state=NORMAL) # set state to normal so that changes can be made to the textbox
    details.delete('1.0', END) #clear whatevers currently in the textbox

    try:
        data = collectInfo()
        row = data[data['name'] == selected]
        appid_info = row["appid"]
        appid = int(appid_info[0])

        #Als de API het niet doet gaat hij om een of andere reden niet naar de except. Vandaar dit
        try:
            game = collectInfo(gameID = appid)
        except:
            pass

        details.insert(END, f'{game["name"]}\n'  # insert all the details into the textbox
                            f'_____________________________\n'  # this ones just for looks
                            f'Developer: {game["developer"]}\n'
                            f'Price: {float(game["price"]) / 100}\n'
                            f'Positive ratings: {game["positive"]}\n'
                            f'Negative ratings: {game["negative"]}\n'
                            f'Average playtime: {game["average_forever"]} minutes\n'
                            f'Owners: {game["owners"]} copies\n'
                            f'Languages: {game["languages"]}')
        showgraph(game['appid'])
    #Zodat de games weergegeven kunnen worden als de API niet werkt
    except:
        sorted_dict = sorted(json_to_dict(data_location), key=lambda k: k['name'])  # sort list of dicts

        start = 0  # yes im going to try and implement a  binary search and im in hell
        end = len(sorted_dict) - 1
        while True:
            middle = (start + end) // 2
            game = sorted_dict[middle]
            if game["name"] > selected:
                end = middle - 1
            elif game["name"] < selected:
                start = middle + 1
            else:
                details.insert(END, f'_____________________________\n'  # this ones just for looks
                                    f'Recent info can\'t be collected. You may look at outdated stats.\n'
                                    f'_____________________________\n'  # this ones just for looks
                                    f'{game["name"]}\n'
                                    f'_____________________________\n'  # this ones just for looks
                                    f'Release date:{game["release_date"]}\n'
                                    f'Developer: {game["developer"]}\n'
                                    f'Price: ${game["price"]}\n'
                                    f'Genres: {game["genres"]}\n'
                                    f'Platforms: {game["platforms"]}\n'
                                    f'Positive ratings: {game["positive_ratings"]}\n'
                                    f'Negative ratings: {game["negative_ratings"]}\n'
                                    f'Average playtime: {game["average_playtime"]} hours\n'
                                    f'Owners: {game["owners"]} copies\n')
                break
        showgraph(0, [game["positive_ratings"], game["negative_ratings"]])
    details.config(state=DISABLED)  # set it back to disabled to the user cant write 'penis' in the textbox



    return None  #python gets mad at me if i dont return anything and i dont know why
    # place i got the code from: https://stackoverflow.com/questions/34327244/binary-search-through-strings



def filterBy(i):  # same as search but like. different
    global current_filter
    selection = current_filter.get()

    if selection == "no filter":
        listInsert(fillList('name'))
        global games_from_list
        games_from_list = gameslist.get(0, "end")

    if selection == "price":
        pricefilterframe.pack(side=RIGHT,pady=5, padx=5)


def filterByPrice(**kwargs):

    sorting = kwargs.get('sort', None)

    if sorting:
        current_sort_label.config(text=f"sorted by: price")
        min_price = -1
        max_price = 10 ** 999 #Lijkt me sterk dat er een spel ooit zo duur zou zijn
        current_sort_label.config(text=f"sorted by: price")
    else:
        min_price = float(pricefrom.get())
        max_price = float(priceto.get())
        current_sort_label.config(text=f"filterd by: price ${format(min_price, '.2f')} - ${format(max_price, '.2f')}")

    gameslist.delete(0, END)


    all_games = collectInfo()

    games_names = all_games["name"]
    games_prices = all_games["price"]

    counter = 0
    games = []
    for i in games_prices:
        games_price = float(i) / 100 #Van centen naar euro's
        if min_price <= games_price <= max_price:
            games.append([games_price, games_names[counter]])
        counter += 1

    for game in sort(games):
        gameslist.insert("end", game[1])



    global games_from_list
    games_from_list = gameslist.get(0, "end")


def search(a):
    query = searchbar.get() #get contents of searchbar

    gameslist.delete(0, END)  # clear listbox
    if query == "":#if searchbar is empty, insert entire list
        listInsert(games_from_list)
        return

    if case_sensitive == True:
        for game in games_from_list:
            if query in game:
                gameslist.insert("end", game)
    else:
        for game in games_from_list:
            no_case = game.lower()
            if query.lower() in no_case:
                gameslist.insert("end", game)

                  #     for loop in binary search


def caseSensitive():
    global case_sensitive
    if case_sensitive == True:
        case_sensitive = False

    elif case_sensitive == False:
        case_sensitive = True


def sortby(i):
    global current_sort
    selection = current_sort.get()
    if selection == "name":
        listInsert(sort(fillList('name')))
        current_sort_label.config(text=f"sorted by: name")
    elif selection == "price":
        filterByPrice(sort = True)


state = 0
def neopixelChange(i):
    global state
    rem = Pyro5.api.Proxy(con)
    selection = current_neopxl.get()
    if selection == "off":
        try:
            if state != 0:
                if state == 1:
                    rem.recieve_smooth(False)
                else:
                    rem.recieve_flash(False)
            rem.change_neo([[0, 0, 0]])
            state = 0
            changeButtonColor(None)
        except:
            time.sleep(2)

    elif selection == "white":
        try:
            if state != 0:
                if state == 1:
                    rem.recieve_smooth(False)
                else:
                    rem.recieve_flash(False)
            rem.change_neo([[255, 255, 255]])
            state = 0
            changeButtonColor(None)
        except:
            time.sleep(2)

    elif selection == "smooth":
        try:
            if state != 0:
                if state == 1:
                    rem.recieve_smooth(False)
                else:
                    rem.recieve_flash(False)
            rem.recieve_smooth(True)
            state = 1
            changeButtonColor(None)
        except:
            time.sleep(2)

    elif selection == "flash":
        try:
            if state != 0:
                if state == 1:
                    rem.recieve_smooth(False)
                else:
                    rem.recieve_flash(False)
            rem.recieve_flash(True)
            state = 2
            changeButtonColor(None)
        except:
            time.sleep(2)

    elif selection == "pick color":
        color = (askcolor((0, 0, 0), root))[0]
        try:
            if state != 0:
                if state == 1:
                    rem.recieve_smooth(False)
                else:
                    rem.recieve_flash(False)
            rem.change_neo([color])
            changeButtonColor(color)
            state = 0
        except:
            time.sleep(2)


def send_wave():
    rem = Pyro5.api.Proxy(con)
    TI_wavebutton.config(state=DISABLED)
    TI_wavebutton.update()
    try:
        rem.recieve_wave()
        time.sleep(4)
    except:
        time.sleep(2)
    finally:
        TI_wavebutton.config(state="normal")
        TI_wavebutton.update()


def thread_send_wave():
    threading.Thread(target=send_wave, daemon=True).start()


def send_beep():
    rem = Pyro5.api.Proxy(con)
    TI_soundbutton.config(state=DISABLED)
    try:
        for i in range(0, 5):
           rem.send_beep()
           time.sleep(1.3)
    except:
        time.sleep(2)
    finally:
        TI_soundbutton.config(state=NORMAL)


def thread_send_beep():
    threading.Thread(target=send_beep, daemon=True).start()


def onExit():
    rem = Pyro5.api.Proxy(con)
    root.destroy()
    threading.Thread(target = rem.shutdown())
    exit()


def fromRGB(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    # bron: https://stackoverflow.com/a/51592104
    return "#%02x%02x%02x" % rgb


def changeButtonColor(color):
      # De rgb kleuren
    if color is None:
        TI_neopixel_options.config(bg="#042430", fg="white",
                                   activebackground='#092F3E',
                                   activeforeground='white',
                                   borderwidth=0,
                                   highlightthickness=0)
    else:
        TI_neopixel_options.config(bg=f"{fromRGB(color)}", activebackground=f"{fromRGB(color)}")
        print(max(color))
        if max(color) >= 200:
            TI_neopixel_options.config(fg='black',activeforeground='black')
        else:
            TI_neopixel_options.config(fg='white', activeforeground='white')


    #-- placing wigdets
root = tix.Tk()
root.config(bg="#042430")
root.iconbitmap("steam_icon.ico") #how the fuck does this slow down the entire app???
root.title("steam application")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", lambda: onExit())
theme = ttk.Style(root)
tooltip_balloon = tix.Balloon(root, bg="#2B526F")



rightframe = Frame(master=root, width=768, height=576,bg="#042430")
rightframe.grid(row=0,column=0, padx=10, pady=10)

# --sort window
settingswindow = Frame(master=rightframe, bg="#042430")
settingswindow.pack(side=TOP, pady=10)


# --wigdets in window

sorting_options = ["sort by", "name", "price", "date"]
global current_sort
current_sort = StringVar()
current_sort.set(sorting_options[0])
global sort_optionmenu
sort_optionmenu = OptionMenu(settingswindow, current_sort, *sorting_options, command=sortby)
sort_optionmenu.config(bg="#042430", fg="white",
                       activebackground='#092F3E',
                       activeforeground='white',
                       borderwidth=0,
                       highlightthickness=0)
sort_optionmenu["menu"].config(bg="#042430", fg="white", activebackground="#0b3a4d")
sort_optionmenu.pack(side=RIGHT, pady=5, padx=5)

filter_options = ('no filter', 'genre', 'platform', 'price')
global current_filter
current_filter = StringVar()
current_filter.set(filter_options[0])
filter_optionmenu = OptionMenu(settingswindow, current_filter, *filter_options, command=filterBy)  # filteroptions
filter_optionmenu.config(bg="#0B3545", fg="white",
                         activebackground='#092F3E',
                         activeforeground='white',
                         borderwidth=0,
                         highlightthickness=0)
filter_optionmenu["menu"].config(bg="#042430", fg="white", activebackground="#0b3a4d")
filter_optionmenu.pack(side=TOP,pady=5, padx=5)

genrefilter_options = ["pick a genre", "Action", "Adventure", "Indie", "RPG", "Early Access"]
global current_genre
current_genre = StringVar()
current_genre.set(genrefilter_options[0])
global genre_optionmenu
genre_optionmenu = OptionMenu(settingswindow, current_genre, *genrefilter_options, )#command=filterByGenre
genre_optionmenu.config(bg="#0B3545", fg="white",
                        activebackground='#092F3E',
                        activeforeground='white',
                        borderwidth=0,
                        highlightthickness=0)
genre_optionmenu["menu"].config(bg="#0B3545", fg="white", activebackground="#0b3a4d")

platformfilter_options = ["pick a platform", "windows", "mac", "linux"]
global current_platform
current_platform = StringVar()
current_platform.set(platformfilter_options[0])
global platform_optionmenu
platform_optionmenu = OptionMenu(settingswindow, current_platform, *platformfilter_options, command=filterByPlatforms)
platform_optionmenu.config(bg="#0B3545", fg="white",
                           activebackground='#092F3E',
                           activeforeground='white',
                           borderwidth=0,
                           highlightthickness=0)
platform_optionmenu["menu"].config(bg="#0B3545", fg="white", activebackground="#0b3a4d")

global pricefilterframe
pricefilterframe = Frame(settingswindow, bg="#042430")
labelfrom = Label(master=pricefilterframe, text="from", bg="#042430", fg="white")
labelfrom.grid(row=0)
global pricefrom
pricefrom = Entry(master=pricefilterframe, bg="#0B3545", fg="white", insertbackground="white", insertwidth=1)
pricefrom.grid(row=1)
labelto = Label(master=pricefilterframe, text="to", bg="#042430", fg="white")
labelto.grid(row=2)
global priceto
priceto = Entry(master=pricefilterframe, bg="#0B3545", fg="white", insertbackground="white", insertwidth=1)
priceto.grid(row=3)
getpricefilter_button = Button(master=pricefilterframe, text="filter", command=filterByPrice, bg="#0B3545", fg="white",
                               borderwidth=0)
getpricefilter_button.grid(row=4, pady=5)


case_button = Checkbutton(master=settingswindow, command=caseSensitive, text=f"Case sensitve", bg="#0B3545", fg="white",
                          selectcolor="#042430", highlightbackground="#0B3545", indicatoron=0, overrelief="sunken")
tooltip_balloon.bind_widget(case_button, balloonmsg='if on, search will be case sensitive.')
case_button.pack(side=BOTTOM, pady=5, padx=5)

# listbox
listframe = Frame(master=rightframe, bg="#0B3545")
searchbarframe= Frame(master=rightframe,bg="#042430")
searchbar = Entry(master=searchbarframe)
searchbar.config(bg="#133d4d", fg="white", insertbackground="white", insertwidth=1) #look i just *do not* like the way the cursors in tkinter looks
searchbar.bind("<Return>", search)
search_label = Label(master=searchbarframe, text="search:", fg="white", bg="#042430")
scrollbar = Scrollbar(listframe, orient="vertical")
gameslist = Listbox(master=listframe, yscrollcommand=scrollbar.set, background="#042430", fg="white",selectbackground="#133d4d",highlightcolor="#133d4d", width=50, activestyle="none")
scrollbar.config(command=gameslist.yview)
gameslist.bind("<<ListboxSelect>>", getDetails)
gameslist.bind("<B1-Leave>", lambda event: "break")
searchbarframe.pack(side="top")
search_label.pack(side="left")
searchbar.pack(side="right")
listframe.pack(side="top")
gameslist.pack(side="left", expand=True, fill="both")
scrollbar.pack(side="right", fill="y")
current_sort_label = Label(master=rightframe, text=f"sorted by: not sorted", fg="white", bg="#042430")
current_sort_label.pack(side="top", fill="x")

detailsframe = Frame(master=rightframe, bg="#0B3545", width=300, height=200)
detailsframe.pack(side='bottom')
detailsframe.pack_propagate(False)
# scrollbar = Scrollbar(detailsframe, orient="vertical")
global details
details = Text(master=detailsframe, bg="#0B3545", fg="white", wrap=WORD)
# details.insert(END, "“According to all known laws of aviation, there is no way that a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyways. Because bees don't care what humans think is impossible.”")
details.config(state=DISABLED)
# scrollbar.config(command=details.yview)
# scrollbar.pack(side="right", fill="y")
details.pack(pady=10)

#--leftframe
leftframe = Frame(master=root)
leftframe.grid(row=0,column=1, padx=10, pady=10)


leftframe_notebook = ttk.Notebook(leftframe)
# leftframe_notebook.config(background="#042430")
ntbk_frame1 = ttk.Frame(leftframe_notebook) 
ntbk_frame2 = ttk.Frame(leftframe_notebook)
rpi_frame = ttk.Frame(leftframe_notebook)
leftframe_notebook.add(ntbk_frame1, text='ratings')
leftframe_notebook.add(rpi_frame, text='raspberry pi')

#rpi_frame
rpilabel = Label(master=rpi_frame,text="raspberry pi functions", fg="white", bg="#0B3545")
rpilabel.grid(row=0, padx=10, pady=10)

TI_wavebutton = Button(master=rpi_frame, text="wave", command=thread_send_wave, bg="#042430",fg="white", borderwidth=0)
tooltip_balloon.bind_widget(TI_wavebutton, balloonmsg='wave to your friend with the servo')
TI_wavebutton.grid(row= 1, padx=10, pady=10)
TI_soundbutton = Button(master=rpi_frame, text="send signal", command=thread_send_beep, bg="#042430",fg="white",borderwidth=0)
tooltip_balloon.bind_widget(TI_soundbutton, balloonmsg='send a sound signal to your friend')
TI_soundbutton.grid(row=1, column=1)
#TI_togglesensor = Button(master=rpi_frame, text="afstandsensor display:neopixel", bg="#042430",fg="white", command=afstandsensordisplay)
sensordisplay = "neopixel"
#TI_togglesensor.grid(row=1, column=2,padx=10)
neopixel_label = Label(master=rpi_frame,text="neopixel functions", fg="white", bg="#0B3545")
neopixel_label.grid(row=3)
neopixel_options = ('off', 'white', 'smooth', 'flash', 'pick color')
current_neopxl = StringVar()
current_neopxl.set(neopixel_options[0])
TI_neopixel_options = OptionMenu(rpi_frame, current_neopxl, *neopixel_options, command=neopixelChange)
TI_neopixel_options["menu"].config(bg="#042430", fg="white", activebackground="#0b3a4d")
print(f"menu parameters{TI_neopixel_options.config()}")
TI_neopixel_options.config(bg="#042430",fg="white",
                           activebackground='#092F3E',
                           activeforeground='white',
                           borderwidth=0,
                           highlightthickness = 0)
tooltip_balloon.bind_widget(TI_neopixel_options, balloonmsg="colors and effects with your ledstrip")

TI_neopixel_options.grid(row=4)
#TI_slider = Scale(master=rpi_frame, from_=0, to=64, tickinterval=64,background="#0B3545", fg='white', troughcolor='#3D6D7F', activebackground='#09192A', highlightthickness=0)
#TI_slider.grid(row=4, column=1,padx=10, pady=10)


#Notebook Style
noteStyler = ttk.Style()

# Import the Notebook.tab element from the default theme
noteStyler.element_create('Plain.Notebook.tab', "from", 'default')
# Redefine the TNotebook Tab layout to use the new element
noteStyler.layout("TNotebook.Tab",
    [('Plain.Notebook.tab', {'children':
        [('Notebook.padding', {'side': 'top', 'children':
            # [('Notebook.focus', {'side': 'top', 'children':
                [('Notebook.label', {'side': 'top', 'sticky': ''})],
            # 'sticky': 'nswe'})],
        'sticky': 'nswe'})],
    'sticky': 'nswe'})])

noteStyler.configure("TNotebook", background="#042430")
noteStyler.configure("TNotebook.Tab", background="#0B3545", foreground="white", lightcolor="#0B3545")
noteStyler.configure("TFrame", background="#0B3545", foreground="white")
# bron: https://stackoverflow.com/questions/22389198/ttk-styling-tnotebook-tab-background-and-borderwidth-not-working

leftframe_notebook.grid()

#--menu
menubar = Menu(root)
helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="Readme", command=openReadme)
root.config(menu=menubar)


##################################################################################################
fig1, ax1 = plt.subplots(figsize=(4, 4))
ax1.pie([1, 0], explode=[0.1, 0], labels=["Positive", "Negative"], autopct='%1.0f%%', shadow=True, startangle=45)
ax1.axis('equal')

canvas = FigureCanvasTkAgg(fig1, master=ntbk_frame2)
canvas.draw()

toolbar = NavigationToolbar2Tk(canvas, ntbk_frame2)
toolbar.update()

canvas.get_tk_widget().pack()
##################################################################################################


caseSensitive()
# showPlaytime()
#showratings()
listInsert(fillList('name'))
games_from_list = gameslist.get(0, "end")
root.mainloop()