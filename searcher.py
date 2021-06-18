import os
import tkinter as tk
from rapidfuzz import fuzz
import time

def Popup(message):  # makes popup to tell user what is correct formatting, stolen from climate change visualizer
    #make a new window
    popup = tk.Tk()
    popup.wm_title("!")

    #make a label with the message
    label = tk.Label(popup, text=message, font=("Helvetica", 10))
    label.pack(side="top", fill="x", pady=20, padx=15)

    #make a button that destroys the popup
    B1 = tk.Button(popup, text="Okay", command=popup.destroy)

    #put the button on screen
    B1.pack()

    #mainloop it
    popup.mainloop()

def Main():  #main
    #starts root
    root = tk.Tk()
    root.wm_title("File Searcher")

    #makes box to input target file
    filelabel = tk.Label(root, text="target file name", pady=10)
    filelabel.pack()
    filebox = tk.Entry(root, width=50, borderwidth=2)
    filebox.pack()

    #makes box to input the directory to search in
    inlabel = tk.Label(root, text="folder to search in", pady=10)
    inlabel.pack()
    inbox = tk.Entry(root, width=50, borderwidth=2, text="inbox")
    inbox.pack()

    #makes scale to select how fuzzy the search will be
    fuzzylabel = tk.Label(root, text="level of fuzziness", pady=5)
    fuzzylabel.pack()
    fuzzyscale = tk.Scale(root, from_=0, to=30, orient="horizontal")
    fuzzyscale.pack()

    #button to submit the input
    submitbutton = tk.Button(root, text="find file", command=lambda: Search(inbox.get(), filebox.get(), fuzzyscale.get()))
    submitbutton.pack()

    #mainloops
    root.mainloop()

def Search(folder, target, fuzziness): #takes 27 secs

    #starts a results list
    resultslist = []

    if not os.path.isdir(folder):  #if the folder to look in is not a thing

        #make a popup telling them
        Popup("invalid folder to search in")
        return

    for root, dirs, files in os.walk(folder):  #make lists of all directories and files

        for filename in files:  #for every file in the list of files

            filename = os.path.splitext(filename)[0]

            if fuzz.ratio(target, filename) >= 100 - fuzziness:  #if the filename is close enough to the target

                #set the current path
                current_path = os.path.normpath(os.path.join(root, filename))

                #add it to the results list
                resultslist.append([current_path, filename])

        for dirname in dirs:  #for every directory in the list of directories

            dirname = os.path.splitext(dirname)[0]

            if fuzz.ratio(target, dirname) >= 100 - fuzziness:  #if the filename is close enough to the target

                #set the current path
                current_path = os.path.normpath(os.path.join(root, dirname))

                #add it to the result list
                resultslist.append([current_path, dirname])

    #display the results page
    ResultsPage(resultslist)

def LISTKEY(list):  #simply to provide a key for the list sort in ResultsPage
    return len(list[0])

def ResultsPage(resultslist):  #displays the results page

    #sort the list to provide relevant answers
    resultslist.sort(key=LISTKEY)


#run the program
Main()

#testfolder location: C:\Users\Sebastien\PycharmProjects\File searcher\testfolder