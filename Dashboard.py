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



# -- functions
def openReadme():
    webbrowser.open('https://github.com/Dave-The-IT-Guy/HUProjectB/blob/main/README.md')

def listInsert(list):
    for item in list:
        gameslist.insert(END, item)


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


def sort_json(location, sort_by):
    # Maak van de json een dict
    dict = json_to_dict(location)

    # Maakt een lijst van alle data die bij de gekozen sleutel hoort
    lst = select(dict, sort_by)

    # Returnt een gesorteerde variant van de lijst
    return sort(lst)


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

    game = kwargs.get('gameID', "all")
    genre = kwargs.get('genre', None)

    if genre != None:
        print("soem")
        url = "https://steamspy.com/api.php?request=genre&genre=" + genre.replace(" ", "+")
    elif game == "all":
        print("all")
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
                            f'Price: ${format((float(game["price"]) / 100), ".2f")}\n'
                            f'Positive ratings: {game["positive"]}\n'
                            f'Negative ratings: {game["negative"]}\n'
                            f'Average playtime: {game["average_forever"]} minutes\n'
                            f'Owners: {game["owners"]} copies\n'
                            f'Languages: {game["languages"]}\n'
                            f'Genres: {game["genre"]}')
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
                                    f'Release date: {game["release_date"]}\n'
                                    f'Developer: {game["developer"]}\n'
                                    f'Price: ${format((game["price"] / 100), ".2f")}\n'
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


def filterByGenre(current_genre):
    gameslist.delete(0, END)

    games = collectInfo(genre = current_genre)
    print(games)

    for name in games["name"]:
        gameslist.insert(END, name)





def filterBy(i):  # same as search but like. different
    global current_filter
    selection = current_filter.get()
    pricefilterframe.grid_forget()
    genre_optionmenu.grid_forget()

    if selection == "no filter":
        listInsert(fillList('name'))
        global games_from_list
        games_from_list = gameslist.get(0, "end")

    elif selection == "price":
        pricefilterframe.grid(row= 0, column=2)

    elif selection == "genre":
        genre_optionmenu.grid(row=0, column=2)


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
sort_optionmenu.config(bg="#0B3545", fg="white",
                       activebackground='#092F3E',
                       activeforeground='white',
                       borderwidth=0,
                       highlightthickness=0)
sort_optionmenu["menu"].config(bg="#042430", fg="white", activebackground="#0b3a4d")
sort_optionmenu.grid(row=0, pady=5, padx=5)

filter_options = ('no filter', 'genre', 'price')
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
filter_optionmenu.grid(row=0, column=1, pady=5, padx=5)

genrefilter_options = ["pick a genre", "Action", "Adventure", "Indie", "RPG", "Early Access"] #UIZOEKEN BESCHIKBARE GENRES
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
case_button = Checkbutton(master=searchbarframe, command=caseSensitive, text=f"Case sensitve", bg="#0B3545", fg="white",
                          selectcolor="#042430", highlightbackground="#0B3545", indicatoron=0, overrelief="sunken")
tooltip_balloon.bind_widget(case_button, balloonmsg='if on, search will be case sensitive.')
searchbarframe.pack(side="top")
search_label.pack(side="left")
case_button.pack(side="right", pady=5, padx=5)
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
rpi_frame = ttk.Frame(leftframe_notebook)
leftframe_notebook.add(ntbk_frame1, text='Ratings')
leftframe_notebook.add(rpi_frame, text='Raspberry PI')

#rpi_frame
rpilabel = Label(master=rpi_frame,text="raspberry pi functions", fg="white", bg="#0B3545")
rpilabel.grid(row=0, padx=10, pady=10)

wave_img = PhotoImage(data="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")
buzzer_img =  PhotoImage(data="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")

TI_wavebutton = Button(master=rpi_frame, text="wave", image=wave_img, command=thread_send_wave, bg="#042430",fg="white", borderwidth=0)
tooltip_balloon.bind_widget(TI_wavebutton, balloonmsg='wave to your friend with the servo')
TI_wavebutton.grid(row= 1, padx=10, pady=10)
TI_soundbutton = Button(master=rpi_frame, text="send signal", image=buzzer_img,command=thread_send_beep, bg="#042430",fg="white",borderwidth=0)
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
neopixel_image =  ImageTk.PhotoImage(Image.open("traffic_light_emoji.png"))
TI_neopixel_options = OptionMenu(rpi_frame, current_neopxl, *neopixel_options, command=neopixelChange)
TI_neopixel_options["menu"].config(bg="#042430", fg="white", activebackground="#0b3a4d")

TI_neopixel_options.config(bg="#042430",fg="white",
                           activebackground='#092F3E',
                           activeforeground='white',
                           borderwidth=0,
                           highlightthickness = 0) #, image=neopixel_image
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


#Laat de diagram zien
fig1, ax1 = plt.subplots(figsize=(4, 4))
ax1.pie([1, 0], explode=[0.1, 0], labels=["Positive", "Negative"], autopct='%1.0f%%', shadow=True, startangle=45)
ax1.axis('equal')

canvas = FigureCanvasTkAgg(fig1, master=ntbk_frame1)
canvas.draw()

toolbar = NavigationToolbar2Tk(canvas, ntbk_frame1)
toolbar.update()

canvas.get_tk_widget().pack()


caseSensitive()
listInsert(fillList('name'))
games_from_list = gameslist.get(0, "end")
root.mainloop()
