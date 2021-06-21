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

    #makes box to put target file in
    filebox = tk.Entry(root, width=50, borderwidth=2)
    filebox.pack()

    #makes box to input the directory to search in
    inlabel = tk.Label(root, text="folder to search in", pady=10)
    inlabel.pack()
    inbox = tk.Entry(root, width=50, borderwidth=2)
    inbox.pack()

    #folders to filter out
    excludelabel = tk.Label(root, text="folders to exclude (A, B)", pady=10)
    excludelabel.pack()
    excludebox = tk.Entry(root, width=50, borderwidth=2)
    excludebox.pack()

    #extensions to filter for
    extensionslabel = tk.Label(root, text="extensions to filter for (.JPG, .PNG)", pady=10)
    extensionslabel.pack()
    extensionslabel = tk.Entry(root, width=50, borderwidth=2)
    extensionslabel.pack()

    #makes scale to select how fuzzy the search will be
    fuzzylabel = tk.Label(root, text="level of fuzziness", pady=5)
    fuzzylabel.pack()
    fuzzyscale = tk.Scale(root, from_=0, to=30, orient="horizontal")
    fuzzyscale.pack()

    #button to submit the input
    submitbutton = tk.Button(root, text="find file", command=lambda: Search(inbox.get(), filebox.get(), fuzzyscale.get(), excludebox.get()))
    submitbutton.pack()

    #mainloops
    root.mainloop()

def Search(folder, target, fuzziness, exclusions): #searches for the files

    #starts a timer
    starttime = time.time()

    #starts a results list
    resultslist = []

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

    else:
        exclusions = [exclusions]

    if not os.path.isdir(folder):  #if the folder to look in is not a thing

        #make a popup telling them
        Popup("invalid folder to search in")
        return

    for root, dirs, files in os.walk(folder, topdown=True):  #make lists of all directories and files

        #removes directories if they're on the exclusion list
        for directory in dirs:
            if directory in exclusions:
                dirs.remove(directory)

        for filename in files:  #for every file in the list of files

            filename = os.path.splitext(filename)[0]

            if fuzz.ratio(target, filename) >= 100 - fuzziness or target.lower() in filename.lower():  #if the filename is close enough to the target

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


    for i in range(0, amount-1):  #for iteration in the amount of results that should be displayed

        #see if it works
        try:

            #add the next shortest result to the results list
            newresults += (resultslist[i][0] + "\n")

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

#implement filters by extension type