from tkinter import *
import webbrowser
# import steam_info
import json
import re

# to do
# search bar
# sort n filter (window)

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
            print(i)
            names.append(i)
    names.sort()

    print(names)

def naam_eerste_spel():
    print("naam")
    #print(naam_eerste_spel())
    dictionary = json_naar_dict()
    print(type(dictionary))
    sorteren(dictionary)


def openSortAndFilterWindow():
    sortwindow = Toplevel(master=root)
    # --sort and filter widgets
    defaultsort = Button(master=sortwind)
    defaultsort.pack()
    print()


def toggleSidebar():
    if sidebar_frame.frame_status:
        sidebar.grid_forget()
        sidebar_frame.frame_status = False
    else:
        sidebar.grid(column=0, row=0, sticky="nesw")
        sidebar_frame.frame_status = True

# def openSidebar():
#     sidebar.pack(expand=True, fill='y', side='right', anchor='nw')
#     sidebar_button.pack_forget()
#     sidebar_button_close.pack(expand=True, fill="y", anchor="n")
#
# def closeSidebar():
#     sidebar_frame.grid_forget()
#     sidebar_button.pack(expand=True, fill="y", anchor="n")
#     sidebar_button_close.pack_forget()
root = Tk()
root.config(bg="#042430")



rightframe = Frame(master=root, width=768, height=576)
rightframe.grid(row=0,column=0, padx=10, pady=10)

listframe = Frame(master=rightframe)
listframe.pack(side="top")
scrollbar = Scrollbar(listframe, orient="vertical")
gameslist = Listbox(master=listframe, yscrollcommand=scrollbar.set)
scrollbar.config(command=gameslist.yview)
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
# img = ImageTk.PhotoImage(Image.open("waluigi.jpg"))
# canv.create_image(20,20, anchor=NW, image=img)
# sometext = Label(master=leftframe, text="some graphs n shit")
# sometext.pack()


#--buttons
sortbutton = Button(master=rightframe, text="sort", command=openSortAndFilterWindow)
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
img = PhotoImage(file = r"C:\Users\Gebruiker\Documents\school\blok 2\pythonProject\yeah.gif")
sidebar_button = Button(sidebar_frame, image=img, command=toggleSidebar, height=400, relief='sunken')
sidebar_button.grid(row=0, column=1, sticky='nswe')


#-- testing
for i in range(0,20):
    gameslist.insert("end", "item #%s" % i)

root.mainloop()