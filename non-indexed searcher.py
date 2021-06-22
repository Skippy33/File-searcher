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

def ToggleSearch(button):  #toggles the extended search button

    if button["text"] == "ON":  #if it says "on"

        #make it say "off"
        button["text"] = "OFF"

    else:  #if it says "off"

        #change it to "on"
        button["text"] = "ON"

def Main():  #main

    #starts root
    root = tk.Tk()

    #change the title of the window
    root.wm_title("File Searcher")

    #makes box to input target file
    filelabel = tk.Label(root, text="target file name", pady=10)
    filelabel.pack()

    #makes box to put target file in
    filebox = tk.Entry(root, width=50, borderwidth=2)
    filebox.pack()

    #makes box to input the directory to search in
    inlabel = tk.Label(root, text="folder to search in", pady=10)
    inlabel.pack()
    inbox = tk.Entry(root, width=50, borderwidth=2)
    inbox.pack()

    #folders to filter out
    excludelabel = tk.Label(root, text="folder paths to exclude (example\A, example\B)", pady=10)
    excludelabel.pack()
    excludebox = tk.Entry(root, width=50, borderwidth=2)
    excludebox.pack()

    #extensions to filter for
    extensionslabel = tk.Label(root, text="extensions to filter for (.JPG, .PNG)", pady=10)
    extensionslabel.pack()
    extensionsbox = tk.Entry(root, width=50, borderwidth=2)
    extensionsbox.pack()

    #make a button to toggle extended searching
    extendedsearchlabel = tk.Label(root, text='extended search (return "snake" for "sna")', pady=10)
    extendedsearchlabel.pack()
    extendedsearchbutton = tk.Button(root, width=15, borderwidth=2, text="ON", command=lambda: ToggleSearch(extendedsearchbutton))
    extendedsearchbutton.pack()

    #makes scale to select how fuzzy the search will be
    fuzzylabel = tk.Label(root, text="level of fuzziness", pady=5)
    fuzzylabel.pack()
    fuzzyscale = tk.Scale(root, from_=0, to=30, orient="horizontal")
    fuzzyscale.pack()

    #button to submit the input
    submitbutton = tk.Button(root, text="find file", command=lambda: Search(inbox.get(), filebox.get(), fuzzyscale.get(), excludebox.get(), extensionsbox.get(), extendedsearchbutton["text"]))
    submitbutton.pack()

    #mainloops
    root.mainloop()

def Search(folder, target, fuzziness, exclusions, extensions, extendedsearch): #searches for the files

    #starts a timer
    starttime = time.time()

    #start the noextensions variable
    noextensions = False

    #starts a results list
    resultslist = []

    #lowercase all extension filters
    extensions = extensions.lower()

    #set an extendedsearch var to tell later programs if it should do an extended search
    if extendedsearch == "ON":  #if it says "on"

        #set the extended search to True
        extendedsearch = True

    else:  #if it says "off"

        #set the extended search to False
        extendedsearch = False

    if exclusions != "":  #if the exclusions list is not empty

        #see if the exclusions can be split
        try:

            #try to split it
            exclusions = exclusions.split(", ")

        # if anything goes wrong
        except BaseException:

            #make a popup
            Popup("improper formatting of exclusions list (should be A, B, C...)")
            return

    else:  #otherwise
        exclusions = [exclusions]

    if extensions != "":  #if the exclusions list is not empty

        #see if the exclusions can be split
        try:

            #try to split it
            extensions = extensions.split(", ")

        # if anything goes wrong
        except BaseException:

            #make a popup
            Popup("improper formatting of extensions list (should be .JPG, .PNG, .HEIC...)")
            return

    else:  #otherwise
        if extensions == "":  #if there are no extensions

            #set the noextensions to True
            noextensions = True

        else: #if there is only 1 extension

            #add it to the list
            extensions = [extensions]

    if not os.path.isdir(folder):  #if the folder to look in is not a thing

        #make a popup telling them
        Popup("invalid folder to search in")
        return

    for root, dirs, files in os.walk(folder, topdown=True):  #make lists of all directories and files

        for filename in files:  #for every file in the list of files

            #set the file extension
            fileextension = os.path.splitext(filename)[1].lower()

            # correct the directory name
            filename = os.path.splitext(filename)[0]

            if fuzz.ratio(target, filename) >= 100 - fuzziness or target.lower() in filename.lower() and extendedsearch:  #if the filename is close enough to the target or the extendedsearch is toggled and it fits for the extended search

                #deals with the extension sorting
                if noextensions == False and fileextension not in extensions:  #if there are extensions to filter by and the file's extension is not on the list
                    continue

                elif noextensions == False and fileextension in extensions:  #if there are extensions to filter by and the file's extension is on the list

                    # set the current path
                    current_path = os.path.normpath(os.path.join(root, filename))

                    # add it to the results list
                    resultslist.append([current_path, filename, fileextension])

                elif noextensions == True:  #if there are no extensions to filter by

                    #set the current path
                    current_path = os.path.normpath(os.path.join(root, filename))

                    #add it to the results list
                    resultslist.append([current_path, filename, fileextension])

        for dirname in dirs:  #for every directory in the list of directories

            if os.path.join(root, dirname) in exclusions:  #if it is on trhe exclusion list

                #BANISH IT
                dirs.remove(dirname)
                continue

            if noextensions or target.lower() in dirname.lower() and extendedsearch and noextensions:  #if there arent any extensions to filter by

                #correct the directory name
                dirname = os.path.splitext(dirname)[0]

                if fuzz.ratio(target, dirname) >= 100 - fuzziness:  #if the filename is close enough to the target

                    #set the current path
                    current_path = os.path.normpath(os.path.join(root, dirname))

                    #add it to the result list
                    resultslist.append([current_path, dirname])

    #gives the length of the search time
    print(str(time.time()-starttime) + " secs to search")

    #display the results page
    ResultsPage(resultslist)

def LISTKEY(list):  #simply to provide a key for the list sort in ResultsPage
    return len(list[0])

def ResultsPage(resultslist):  #displays the results page

    #sort the list to provide relevant answers
    resultslist.sort(key=LISTKEY)

    #make a new window
    results = tk.Tk()
    results.wm_title("Results")

    #make a label with the message
    label = tk.Label(results, text="Amount of displayed results", font=("Helvetica", 10))
    label.pack(side="top", fill="x", pady=5, padx=5)

    #add a scale to change how many results are shown
    resultsscale = tk.Scale(results, from_=5, to=20, orient="horizontal")
    resultsscale.pack()

    #add a display widget
    resultsdisplay = tk.Text(results, height=resultsscale.get(), width=50)
    resultsdisplay.pack()

    #Update the results
    UpdateResults(resultsdisplay, resultslist, resultsscale.get())

    #button to update the results page
    updatebutton = tk.Button(results, text="update results", command=lambda: UpdateResults(resultsdisplay, resultslist, resultsscale.get()))
    updatebutton.pack()

    #mainloop it
    results.mainloop()

def UpdateResults(resultsdisplay, resultslist, amount):  #updates the results page

    #delete all characters in the results page to wipe the canvas
    resultsdisplay.delete("1.0", "end")

    #start a string for the new results
    newresults = ""

    if resultslist == []: #if the results are empty

        #change it to say nothing was found
        newresults = "nothing was found"

        # change the width/height to be correct
        resultsdisplay["width"] = len(max(newresults.split("\n"), key=len)) + 5
        resultsdisplay["height"] = amount

        # insert the new results
        resultsdisplay.insert(tk.END, newresults)
        return


    for i in range(0, amount):  #for iteration in the amount of results that should be displayed

        #see if it works
        try:

            #add the next shortest result to the results list
            newresults += (resultslist[i][0] + resultslist[i][2] + "\n")

        #if there arent enough results, break the loop
        except IndexError:
            break

    #change the width/height to be correct
    resultsdisplay["width"] = len(max(newresults.split("\n"), key=len)) + 5
    resultsdisplay["height"] = amount

    #insert the new results
    resultsdisplay.insert(tk.END, newresults)

#run the program
Main()

#testfolder location: C:\Users\Sebastien\PycharmProjects\File searcher\testfolder
# 30 second search for C drive (fast SSD), 8 minute search for A drive
#sort the eventual indexed version by length of file name, allows for fast binary searching