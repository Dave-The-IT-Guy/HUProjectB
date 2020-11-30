from tkinter import *
import webbrowser
# import steam_info
import json
import re

# to do
# search bar
# sort n filter (window)
# create executable

# -- globals
global game_names
game_names = []
global case_sensitive
case_sensitive = True

# -- functions
def openReadme():
    webbrowser.open('https://github.com/Dave-The-IT-Guy/HUProjectB/blob/main/README.md')



def json_naar_dict():
    #Open het json bestand
    with open('steam.json', 'r') as jsonFile:
        #Sla de inhoud op als dict
        dictFile = json.load(jsonFile)
    return dictFile


def sorteren(unsortedDict):
    #Maak een lege lijst aan voor de namen
    names = []
    #Loop door de dictionaries in de lijst
    for i in unsortedDict:
        #Haal de waarde van de name key uit de dict
        i = i['name']
        #Maak er een string van
        i = str(i)
        #Haal met regex de meeste speciale karakters eruit
        i = re.sub('[^A-Za-z0-9$()\&\+\'\:\w\-\s\.]+', '', i) #[^A-Za-z0-9]

        #Haal alle onnodige spaties weg
        i = " ".join(i.split())
        #Haal wat extra rotzooi uit de string
        (i).replace('()', '')
        i.strip()

        #Als een string met ' begint en eindigd verwijder deze dan
        if i.startswith('\'') == True and i.endswith('\'') == True:
            i = i[1:(len(i) - 1)]
        #Onderstaande code Werkt nog niet helemaal. De laatste conditie moet aangepast worden anders worden bij sommige titles de naam aangepast terwijl dat niet de bedoeling is...
        if i.startswith('(') == True and i.endswith(')') == True and i.count('(') < 2:
            i = i[1:(len(i) - 1)]
        # Als de string niet false is voeg hem toe aan de lijst (strings kunnen false zijn als ze bijv. leeg zijn)
        if i:
            # print(i)
            names.append(i)
    names.sort()

    # print(names)

def naam_eerste_spel():
    print("naam")
    #print(naam_eerste_spel())
    dictionary = json_naar_dict()
    print(type(dictionary))
    sorteren(dictionary)


def openSortAndFilterWindow():
    # --sort window
    sorting = StringVar()
    settingswindow = Toplevel(master=root)
    sortframe = Frame(master=settingswindow)
    sortframe.grid(row=0, column=0)


    sort_by = Label(master=sortframe, text="Sort by(not functional):")
    sort_by.grid(row=0, column=0)
    defaultsort = Radiobutton(master=sortframe, variable=sorting,value="none", text="None")
    defaultsort.grid(row=1, column=0)
    namesort = Radiobutton(master=sortframe, variable=sorting, value="name", text="Name")
    namesort.grid(row=2, column=0)
    settings_label = Label(master=settingswindow, text="Settings")
    settings_label.grid(row=3, column=1)
    case_button = Checkbutton(master=settingswindow, command=caseSensitive, text=f"Case sensitve")
    case_button.grid(row=4, column=1)




def toggleSidebar():
    if sidebar_frame.frame_status:
        sidebar.grid_forget()
        sidebar_frame.frame_status = False
    else:
        sidebar.grid(column=0, row=0, sticky="nesw")
        sidebar_frame.frame_status = True


def listInsert():
    for item in game_names:
        gameslist.insert(END, item)


def search(a):
    query = searchbar.get()
    gameslist.delete(0, END)

    if query == "":
        listInsert()

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

    listInsert()
    







root = Tk()
root.config(bg="#042430")
# root.iconbitmap("steam_icon.ico") #how the fuck does this slow down the entire app???
root.title("steam application")


rightframe = Frame(master=root, width=768, height=576)
rightframe.grid(row=0,column=0, padx=10, pady=10)

listframe = Frame(master=rightframe)
searchbar = Entry(master=rightframe)
searchbar.bind("<Return>", search)
scrollbar = Scrollbar(listframe, orient="vertical")
gameslist = Listbox(master=listframe, yscrollcommand=scrollbar.set)
scrollbar.config(command=gameslist.yview)
searchbar.pack(side="top")
listframe.pack(side="top")
gameslist.pack(side="left", expand=True, fill="both")
scrollbar.pack(side="right", fill="y")

detailsframe = Frame(master=rightframe, bg="#0B3545", width=300, height=200)
detailsframe.pack(side='bottom')
detailsframe.pack_propagate(False)
scrollbar = Scrollbar(detailsframe, orient="vertical")
details = Text(master=detailsframe, bg="#0B3545", fg="white")
details.insert(END, "“According to all known laws of aviation, there is no way that a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyways. Because bees don't care what humans think is impossible.”")
details.config(state=DISABLED)
scrollbar.config(command=details.yview)
scrollbar.pack(side="right", fill="y")
details.pack(pady=10)

#--
leftframe = Frame(master=root)
leftframe.grid(row=0,column=1, padx=10, pady=10)
canv = Canvas(master=leftframe)
canv.pack()



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
sidebar = Frame(sidebar_frame, width=200, bg='#0B3545', height=400, relief='sunken')
sidebar_frame.frame_status = False
img = PhotoImage(file = "yeah.gif")
sidebar_button = Button(sidebar_frame, image=img, command=toggleSidebar, height=400, relief='sunken')
sidebar_button.grid(row=0, column=1, sticky='nswe')

# filling list
for item in json_naar_dict():
    game_names.append(item["name"])

#-- testing
# for i in range(0,20):
#     gameslist.insert("end", "item #%s" % i)
#

# print(testlist)

caseSensitive()
listInsert()
root.mainloop()