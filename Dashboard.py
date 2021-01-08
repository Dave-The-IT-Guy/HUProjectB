# steam project dashboard - verona kragten

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
global game_names
game_names = []
global case_sensitive
case_sensitive = True
global sorting
global sortedgames
sortedgames = game_names
global sensordisplay
sensordisplay = "neopixel"
####Locatie van de steamdata
###data_location = 'steam.json'
#Voor de verbinding met de server
con = "PYRO:steam.functions@192.168.192.24:9090"

# -- to do
# make graph blue
# make it so that TI frame gets placed over GUI
# if i search for someting it undoes the sorting go fix that #edit: fixed it but i havent tested if it works with evertything #edit: undoes the filtering i hate myself
# add a filtering functionality
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

def json_to_dict(location):
    #Open de json file en zet alle in een dictonairy
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

        ## Onderstaande code Werkt nog niet helemaal. De laatste conditie moet aangepast worden anders worden bij sommige titles de naam aangepast terwijl dat niet de bedoeling is...
        #if i.startswith('(') == True and i.endswith(')') == True and i.count('(') < 2:
        #    i = i[1:(len(i) - 1)]

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



def getDetails(i):
    selected = gameslist.get(gameslist.curselection()) # get the current selection in the listbox
    details.config(state=NORMAL) # set state to normal so that changes can be made to the textbox
    details.delete('1.0', END) #clear whatevers currently in the textbox

    sorted_dict = sorted(sort_json(data_location, 'name'), key=lambda k: k['name'])   # sort list of dicts
    start = 0  # yes im going to try and implement a  binary search and im in hell
    end = len(sorted_dict) - 1
    while start <= end:
        middle = (start + end)// 2
        game = sorted_dict[middle]
        if game["name"] > selected:
            end = middle - 1
        elif game["name"] < selected:
            start = middle + 1
        else:
            details.insert(END, f'{game["name"]}\n'  # insert all the details into the textbox
                                '_____________________________\n'  # this ones just for looks
                                f'release date:{game["release_date"]}\n'
                                f'developer: {game["developer"]}\n'
                                f'price: {game["price"]}\n'
                                f'genres: {game["genres"]}\n'
                                f'platforms: {game["platforms"]}\n'
                                f'positive ratings: {game["positive_ratings"]}\n '
                                f'negative ratings: {game["negative_ratings"]}\n'
                                f'average playtime: {game["average_playtime"]} hours\n'
                                f'owners: {game["owners"]} copies\n')

            details.config(state=DISABLED)  # set it back to disabled to the user cant write 'penis' in the textbox
            return None  #python gets mad at me if i dont return anything and i dont know why
    # place i got the code from: https://stackoverflow.com/questions/34327244/binary-search-through-strings

def openSortAndFilterWindow():
    # --sort window
    settingswindow = Toplevel(master=root, bg="#0B3545")
    settingswindow.resizable(False, False)
    settingswindow.geometry("350x200")
    settingswindow.wm_attributes("-topmost", 1)

    # --wigdets in window
    steamlogo_img = ImageTk.PhotoImage(Image.open("steam_logo.png"))
    steamlogo = Label(master=settingswindow, image=steamlogo_img, compound=CENTER)
    steamlogo.place()
    sorting_options = ["sort by","name", "price", "date"]
    global current_sort
    current_sort = StringVar()
    current_sort.set(sorting_options[0])
    global sort_optionmenu
    sort_optionmenu = OptionMenu(settingswindow, current_sort, *sorting_options, command=sortby)
    sort_optionmenu.config(bg="#042430",fg="white",
                           activebackground='#092F3E',
                            activeforeground='white',
                           borderwidth=0,
                           highlightthickness = 0)
    sort_optionmenu["menu"].config(bg="#042430",fg="white", activebackground="#0b3a4d")
    sort_optionmenu.grid(row=0,column=0, pady=10, padx=10)

    filter_options = ('no filter', 'genre', 'platform', 'price')
    global current_filter
    current_filter = StringVar()
    current_filter.set(filter_options[0])
    filter_optionmenu = OptionMenu(settingswindow, current_filter, *filter_options, command=filterBy)#filteroptions
    filter_optionmenu.config(bg="#042430",fg="white",
                           activebackground='#092F3E',
                            activeforeground='white',
                           borderwidth=0,
                           highlightthickness = 0)
    filter_optionmenu["menu"].config(bg="#042430",fg="white", activebackground="#0b3a4d")
    filter_optionmenu.grid(row=0, column=1)

    genrefilter_options = ["pick a genre","Action", "Adventure", "Indie", "RPG", "Early Access"]
    global current_genre
    current_genre = StringVar()
    current_genre.set(genrefilter_options[0])
    global genre_optionmenu
    genre_optionmenu = OptionMenu(settingswindow, current_genre, *genrefilter_options, command=filterByGenre)
    genre_optionmenu.config(bg="#042430",fg="white",
                           activebackground='#092F3E',
                            activeforeground='white',
                           borderwidth=0,
                           highlightthickness = 0)
    genre_optionmenu["menu"].config(bg="#042430",fg="white", activebackground="#0b3a4d")

    platformfilter_options = ["pick a platform","windows", "mac", "linux"]
    global current_platform
    current_platform = StringVar()
    current_platform.set(platformfilter_options[0])
    global platform_optionmenu
    platform_optionmenu = OptionMenu(settingswindow, current_platform, *platformfilter_options, command=filterByPlatforms)
    platform_optionmenu.config(bg="#042430",fg="white",
                           activebackground='#092F3E',
                            activeforeground='white',
                           borderwidth=0,
                           highlightthickness = 0)
    platform_optionmenu["menu"].config(bg="#042430",fg="white", activebackground="#0b3a4d")

    global pricefilterframe
    pricefilterframe = Frame(settingswindow, bg="#0B3545")
    labelfrom =  Label(master=pricefilterframe,text="from", bg="#0B3545",fg="white")
    labelfrom.pack()
    global pricefrom
    pricefrom = Entry(master=pricefilterframe, bg="#042430", fg="white", insertbackground="white", insertwidth=1)
    pricefrom.pack()
    labelto = Label(master=pricefilterframe, text="to", bg="#0B3545",fg="white")
    labelto.pack()
    global priceto
    priceto = Entry(master=pricefilterframe, bg="#042430", fg="white", insertbackground="white", insertwidth=1)
    priceto.pack()
    getpricefilter_button = Button(master=pricefilterframe, text="filter", command=filterByPrice, bg="#042430",fg="white",borderwidth=0)
    getpricefilter_button.pack(pady=10)

    settings_label = Label(master=settingswindow, text="search", bg="#0B3545", fg="white")
    settings_label.grid(row=3, column=1)
    case_button = Checkbutton(master=settingswindow, command=caseSensitive, text=f"Case sensitve", bg="#0B3545", fg="white", selectcolor="#042430", highlightbackground="#0B3545", indicatoron=0, overrelief="sunken")
    tooltip_balloon.bind_widget(case_button, balloonmsg='if on, search will be case sensitive.')
    case_button.grid(row=4, column=1)



def filterBy(i):  # same as search but like. different
    global current_filter
    selection = current_filter.get()

    pricefilterframe.grid_forget()
    genre_optionmenu.grid_forget()
    pricefilterframe.grid_forget()


    if selection == "no filter":
        listInsert(sortedgames)

    if selection == "genre":
        genre_optionmenu.grid(row=0, column=2, pady=10, padx=10)

    if selection == "platform":
        platform_optionmenu.grid(row=0, column=2, pady=10, padx=10)

    if selection == "price":
        pricefilterframe.grid(row=0, column=2, pady=10, padx=10)


def filterByGenre(i):
    selection = current_genre.get()
    gameslist.delete(0, END)
    if selection == "pick a genre":
       listInsert(sortedgames)
    else:
        for game in json_to_dict(): #looks at selection and compares it to every game[genres]
            if selection in game["genres"]:
                gameslist.insert("end", game["name"])

def filterByPrice():
    selectionfrom = float(pricefrom.get())
    selectionto = float(priceto.get())
    gameslist.delete(0, END)
    for game in json_to_dict():
        if selectionfrom <= game["price"] <= selectionto:
            gameslist.insert("end", game["name"])


def filterByPlatforms(i):
    gameslist.delete(0, END)
    selection = current_platform.get()
    if selection == "pick a platform":
        listInsert(sortedgames)
    else:
        for game in json_to_dict():
            if selection in game["platforms"]:
                gameslist.insert("end", game["name"])




def search(a):
    query = searchbar.get() #get contents of searchbar

    gameslist.delete(0, END)  # clear listbox
    if query == "":#if searchbar is empty, insert entire list
        listInsert(sortedgames)

    if case_sensitive == True:
        for game in sortedgames:
            if query in game:
                gameslist.insert("end", game)
    else:
        for game in sortedgames:
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

#def sortby(i):
#    global current_sort
#    selection = current_sort.get()
#    if selection == "name":
#        sortByName()
#    elif selection == "date":
#        sortByDate()
#    elif selection == "price":
#        sortByPrice()
#    else:
#        sortByNone()

#def sortByNone():
#    gameslist.delete(0, END)
#    listInsert(game_names)
#    current_sort_label.config(text=f"sorted by: not sorted")
#
#def sortByName():
#    gameslist.delete(0, END)
#    global sortedgames
#    sortedgames = sort("1") #get the sorted list
#    listInsert(sortedgames)#and put it in the listbox
#    current_sort_label.config(text=f"sorted by: name")
#
#def sortByPrice():
#    gameslist.delete(0, END)
#    global sortedgames
#    sortedgames = sort("2")
#    listInsert(sortedgames)
#    current_sort_label.config(text=f"sorted by: price")
#
#def sortByDate():
#    gameslist.delete(0, END)
#    global sortedgames
#    sortedgames = sort("3")
#    listInsert(sortedgames)
#    current_sort_label.config(text=f"sorted by: release date")
#    current_sort = "date"


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


def showgraph():
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'Goed', 'Slecht'
    sizes = [900, 100]
    explode = (0, 0.1)

    fig1, ax1 = plt.subplots(figsize=(4, 4))
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.0f%%', shadow=True, startangle=45)
    ax1.axis('equal')


    canvas = FigureCanvasTkAgg(fig1, master=leftframe1)
    canvas.draw()
    toolbar = NavigationToolbar2Tk(canvas, leftframe1)
    toolbar.update()

    canvas.get_tk_widget().pack()


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
            TI_neopixel_options.config(bg=f"{fromRGB(color)}", activebackground=f"{fromRGB(color)}")
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
current_sort_label = Label(master=rightframe, text=f"sorted by: name", fg="white", bg="#042430")
current_sort_label.pack(side="top", fill="x")

detailsframe = Frame(master=rightframe, bg="#0B3545", width=300, height=200)
detailsframe.pack(side='bottom')
detailsframe.pack_propagate(False)
# scrollbar = Scrollbar(detailsframe, orient="vertical")
global details
details = Text(master=detailsframe, bg="#0B3545", fg="white")
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
leftframe1 = ttk.Frame(leftframe_notebook)   # first page, which would get widgets gridded into it
rpi_frame = ttk.Frame(leftframe_notebook)   # second page
leftframe_notebook.add(leftframe1, text='graph')
leftframe_notebook.add(rpi_frame, text='raspberry pi')

#rpi_frame
rpilabel = Label(master=rpi_frame,text="raspberry pi functions", fg="white", bg="#0B3545")
rpilabel.grid(row=0, padx=10, pady=10)
rpilabel = Label(master=rpi_frame,text="geluids sensor", fg="white", bg="#0B3545")
rpilabel.grid(row=0, column=1)

TI_wavebutton = Button(master=rpi_frame, text="zwaai", command=thread_send_wave, bg="#042430",fg="white", borderwidth=0)
tooltip_balloon.bind_widget(TI_wavebutton, balloonmsg='zwaai naar je je vriend via de servo')
TI_wavebutton.grid(row= 1, padx=10, pady=10)
TI_soundbutton = Button(master=rpi_frame, text="geluidsignaal geven", command=thread_send_beep, bg="#042430",fg="white",borderwidth=0)
tooltip_balloon.bind_widget(TI_soundbutton, balloonmsg='stuur een piep naar je vriend')
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

#--buttons
sortbutton = Button(master=rightframe, text="settings", command=openSortAndFilterWindow, bg="#03202b", fg="white", borderwidth=0, highlightcolor="#092F3E", overrelief="sunken")
tooltip_balloon.bind_widget(sortbutton, balloonmsg='more settings for searching \nthrough the list of games')
sortbutton.pack()

#--menu
menubar = Menu(root)
helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="Readme", command=openReadme)
root.config(menu=menubar)





threading.Thread(target=caseSensitive, daemon=True).start()
#caseSensitive()
showgraph()
listInsert(sort_json(data_location, 'name'))
root.mainloop()
