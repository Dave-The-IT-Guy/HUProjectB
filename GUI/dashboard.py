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



# to do
# do a binry search for getting the details
# make graph blue
#slider in TI (0-64)
# make it so that TI frame gets placed over GUI

# -- globals
global game_names
game_names = []
global case_sensitive
case_sensitive = True
global sorting

# -- functions
def openReadme():
    webbrowser.open('https://github.com/Dave-The-IT-Guy/HUProjectB/blob/main/README.md')



def json_naar_dict():
    global steamdata
    # json file openen
    with open('steam.json') as json_file:
        #json naar lijst
        steamdata = json.load(json_file)
        # #lijst naar dict
        # steamdata = new_dict = dict((item['appid'], item) for item in steamdata_list)
        return steamdata

def sorteren(categorie_input):
    global gesorteerd
    json_naar_dict()
    # laat de gebruiker kiezen waar hij op sorteerd
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
        gesorteerd_names = []#alleen de namen terug geven
        for i in gesorteerd:
            shown_name: ""
            shown_name = i["name"]
            gesorteerd_names.append(shown_name)
        return gesorteerd_names
    elif categorie_input == '3':
        # sorteer op de prijs
        gesorteerd = sorted(steamdata, key=lambda k: k['price'], reverse=False)
        gesorteerd_names = []
        for i in gesorteerd:
            shown_name: ""
            shown_name = i["name"]
            gesorteerd_names.append(shown_name)
        return gesorteerd_names

def naam_eerste_spel():
    print("naam")
    #print(naam_eerste_spel())
    dictionary = json_naar_dict()
    print(type(dictionary))
    sorteren(dictionary)

def getDetails(i):
    selected = gameslist.get(gameslist.curselection()) # get the current selection in the listbox
    details.config(state=NORMAL) # set state to normal so that changes can be made to the textbox
    details.delete('1.0', END) #clear whatevers currently in the textbox
    for game in json_naar_dict():
        if game["name"] == selected :#too lazy for a binary search, it works fine :~)
            details.insert(END, f'{game["name"]}\n')
            details.insert(END, '_____________________________\n\n')
            details.insert(END,f'release date:{game["release_date"]}\n')
            details.insert(END,f'developer: {game["developer"]}\n')
            details.insert(END,f'price: {game["price"]}\n')
            details.insert(END, f'genres: {game["genres"]}\n')
            details.insert(END, f'platforms: {game["platforms"]}\n')
            details.insert(END, f'positive ratings: {game["positive_ratings"]}\n')
            details.insert(END, f'negative ratings: {game["negative_ratings"]}\n')
            details.insert(END, f'average playtime: {game["average_playtime"]} hours\n')
            details.insert(END, f'owners: {game["owners"]} copies\n')

            details.config(state=DISABLED)  # set it back to disabled to the user cant write 'penis' in the textbox
            return None
    print("no matches found")






def openSortAndFilterWindow():
    # --sort window
    sorting = StringVar()
    settingswindow = Toplevel(master=root)
    sortframe = Frame(master=settingswindow)
    sortframe.grid(row=0, column=0)

    # --wigdets in window
    sort_by = Label(master=sortframe, text="Sort by:")
    sort_by.grid(row=0, column=0)
    defaultsort = Radiobutton(master=sortframe, variable=sorting,value="none", text="None", command=sortByNone)
    defaultsort.grid(row=1, column=0)
    namesort = Radiobutton(master=sortframe, variable=sorting, value="name", text="Name", command=sortByName)
    namesort.grid(row=2, column=0)
    pricesort = Radiobutton(master=sortframe, variable=sorting, value="price", text="price", command=sortByPrice)
    pricesort.grid(row=3, column=0)
    datesort = Radiobutton(master=sortframe, variable=sorting, value="date", text="date", command=sortByDate)
    datesort.grid(row=4, column=0)

    settings_label = Label(master=settingswindow, text="other Settings:")
    settings_label.grid(row=3, column=1)
    case_button = Checkbutton(master=settingswindow, command=caseSensitive, text=f"Case sensitve")
    case_button.grid(row=4, column=1)




def toggleSidebar():#i havent put anything in here yet
    if sidebar_frame.frame_status:
        sidebar.grid_forget()
        sidebar_frame.frame_status = False
    else:
        sidebar.grid(column=0, row=0, sticky="nesw")
        sidebar_frame.frame_status = True


def listInsert(list):
    for item in list:
        gameslist.insert(END, item)

def search(a):
    query = searchbar.get() #get contents of searchbar

    gameslist.delete(0, END)  # clear listbox
    if query == "":#if searchbar is empty, insert entire list
        listInsert(game_names)

    if case_sensitive == True:
        for game in game_names:
            if query in game:
                gameslist.insert("end", game)
    else:
        for game in game_names:
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



def sortByNone():
    gameslist.delete(0, END)
    listInsert(game_names)
    current_sort_label.config(text=f"sorted by: not sorted")

def sortByName():
    gameslist.delete(0, END)
    sortedgames = sorteren("1") #get the sorted list
    listInsert(sortedgames)#and put it in the listbox
    current_sort_label.config(text=f"sorted by: name")

def sortByPrice():
    gameslist.delete(0, END)
    sortedgames = sorteren("2")
    listInsert(sortedgames)
    current_sort_label.config(text=f"sorted by: price")

def sortByDate():
    gameslist.delete(0, END)
    sortedgames = sorteren("3")
    listInsert(sortedgames)
    current_sort_label.config(text=f"sorted by: release date")

def showgraph():
    t = [1, 2, 3, 4, 5, 6]
    s = [1, 2, 3, 4, 5, 6]
    testgraph = plt.Figure(figsize=(5, 4), dpi=100)
    testgraph.add_subplot(111).plot(t,s)

    canvas = FigureCanvasTkAgg(testgraph, master=leftframe1)
    canvas.draw()
    toolbar = NavigationToolbar2Tk(canvas, leftframe1)
    toolbar.update()

    fig, ax = plt.subplots(facecolor="#042430")
    ax.set_facecolor('#0B3545')
    ax.set_title('Voltage vs. time chart', color='white')
    ax.set_xlabel('time (s)', color='white')
    ax.set_ylabel('voltage (mV)', color='white')
    ax.plot(t, s, 'xkcd:crimson')
    ax.plot(t, s, color='C4', linestyle='--')
    ax.tick_params(labelcolor='white')

    canvas.get_tk_widget().pack()

def neopixelChange(i):
    selection = current_neopxl.get()
    if selection == "off":
        print(selection)
    if selection == "pick color":
        print(askcolor((255, 255, 0), root))



#-- placing wigdets
root = Tk()
root.config(bg="#042430")
# root.iconbitmap("steam_icon.ico") #how the fuck does this slow down the entire app???
root.title("steam application")
theme = ttk.Style(root)
theme.theme_use('xpnative')
print(ttk.Style().theme_names())

rightframe = Frame(master=root, width=768, height=576,bg="#042430")
rightframe.grid(row=0,column=0, padx=10, pady=10)

listframe = Frame(master=rightframe, bg="#0B3545")
searchbarframe= Frame(master=rightframe,bg="#042430")
searchbar = Entry(master=searchbarframe)
searchbar.config(bg="#133d4d")
searchbar.bind("<Return>", search)
search_label = Label(master=searchbarframe, text="search:", fg="white", bg="#042430")
scrollbar = Scrollbar(listframe, orient="vertical")
gameslist = Listbox(master=listframe, yscrollcommand=scrollbar.set, background="#042430", fg="white",selectbackground="#133d4d",highlightcolor="#133d4d", width=50, activestyle="none")
scrollbar.config(command=gameslist.yview)
gameslist.bind("<<ListboxSelect>>", getDetails)
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
scrollbar = Scrollbar(detailsframe, orient="vertical")
global details
details = Text(master=detailsframe, bg="#0B3545", fg="white")
# details.insert(END, "“According to all known laws of aviation, there is no way that a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyways. Because bees don't care what humans think is impossible.”")
details.config(state=DISABLED)
scrollbar.config(command=details.yview)
scrollbar.pack(side="right", fill="y")
details.pack(pady=10)

#--leftframe
leftframe = Frame(master=root)
leftframe.grid(row=0,column=1, padx=10, pady=10)


leftframe_notebook = ttk.Notebook(leftframe)
# leftframe_notebook.config(background="#042430")
leftframe1 = ttk.Frame(leftframe_notebook)   # first page, which would get widgets gridded into it
leftframe2 = ttk.Frame(leftframe_notebook)   # second page
leftframe_notebook.add(leftframe1, text='graph')
leftframe_notebook.add(leftframe2, text='Two')
#
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

#
leftframe_notebook.grid()

#--buttons
sortbutton = Button(master=rightframe, text="settings", command=openSortAndFilterWindow)
sortbutton.pack()


#--menu
menubar = Menu(root)
helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="Readme", command=openReadme)
root.config(menu=menubar)




#--sidebar
sidebar_frame = Frame(root)
sidebar_frame.grid(column=2, row=0)
sidebar = Frame(sidebar_frame, bg='#0B3545', relief='sunken')
sidebar_frame.frame_status = False
img = PhotoImage(file = "open_friendlist_button.gif")
sidebar_button = Button(sidebar_frame, image=img, command=toggleSidebar, height=450, relief='raised')
sidebar_button.grid(row=0, column=1, sticky='nswe')

    # shit inside the sidebar
sidebarlabel = Label(master=sidebar,text="                       raspberry pi functions", fg="white", bg="#0B3545")
sidebarlabel.grid(row=0, padx=10, pady=10)
TI_button1 = Button(master=sidebar, text="button 1",bg="#042430",fg="white")
TI_button1.grid(row= 1, padx=10, pady=10)
TI_button2 = Button(master=sidebar, text="button 2", bg="#042430",fg="white")
TI_button2.grid(row=1, column=1)
neopixel_options = ('off', 'white', 'pick color')
current_neopxl = StringVar()
current_neopxl.set(neopixel_options[0])
TI_neopixel_options = OptionMenu(sidebar, current_neopxl, *neopixel_options, command=neopixelChange)
TI_neopixel_options["menu"].config(bg="#042430", fg="white")
TI_neopixel_options.grid(row=2)
TI_slider = Scale(master=sidebar, from_=0, to=64)
TI_slider.grid(row=2, column=1,padx=10, pady=10)



# filling list
for item in json_naar_dict():
    game_names.append(item["name"])

#-- testing
# for i in range(0,20):
#     gameslist.insert("end", "item #%s" % i)
#

# print(testlist)

caseSensitive()
showgraph()
listInsert(game_names)
root.mainloop()