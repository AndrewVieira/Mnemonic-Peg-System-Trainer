import tkinter as tk
from tkinter import ttk

import linecache
import random
#from random import randint

TITLE_FONT = ("Helvetica", 24, "bold")
#LIST_FONT = ("

class MnemonicPegSystemApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Mnemonic Peg System Trainer")
        #self.resizable(width=False, height=False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Trainer Variables
        self.selection = []
        self.number_of_items = 10
        self.difficulty = 1

        self.number_correct = 0

        #Handle the diffrent frames used throughout the program
        self.frames = {}

        for frame in (StartPage, MemorizePage, RecallPage, ResultsPage):
            page_name = frame.__name__
            frame = frame(parent=container, controller=self)
            self.frames[page_name] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        frame.when_raised()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        #Grid Configurement
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        
        #Title
        self.titleLabel = ttk.Label(self, text="Mnemonic Peg System Trainer", font=TITLE_FONT)
        self.titleLabel.grid(row=0, column=0, columnspan=5, padx=5, pady=5)
        #.grid(row=0, column=2, columnspan=2, rowspan=2, sticky=W+E+N+S, padx=5, pady=5)

        #Difficulty
        self.difficultyLabel = ttk.Label(self, text="Difficulty:")
        self.difficultyLabel.grid(row=1, column=0, sticky="E", pady=5)
        self.difficulty = tk.IntVar()
        self.difficulty.set(1)
        self.easyRadiobutton = ttk.Radiobutton(self, text="Easy", variable=self.difficulty, value=1).grid(row=1, column=1, pady=5)
        self.mediumRadiobutton = ttk.Radiobutton(self, text="Medium", variable=self.difficulty, value=2).grid(row=1, column=2, pady=5)
        self.hardRadioButton = ttk.Radiobutton(self, text="Hard", variable=self.difficulty, value=3).grid(row=1, column=3, pady=5)
        self.veryHardRadiobutton = ttk.Radiobutton(self, text="Very Hard", variable=self.difficulty, value=4).grid(row=1, column=4, pady=5)
        
        #Number of Items
        vcmd = (self.register(self.validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.entryLabel = ttk.Label(self, text="Number of Items:")
        self.entryLabel.grid(row=2, column=1, sticky="", pady=5)
        self.memoryEntry = ttk.Entry(self, validate="key", validatecommand=vcmd)
        self.memoryEntry.grid(row=2, column=2, columnspan=2, sticky="NSEW", pady=5)
         
        #Begin!
        self.beginButton = ttk.Button(self, text="Begin Training",
                            command=lambda: self.begin())
        self.beginButton.grid(row=3, column=1, columnspan=3, sticky="NSEW", pady=5)

    def when_raised(self):
        self.memoryEntry.insert(tk.END, "10")
        
    def begin(self):
        self.controller.number_of_items = int(self.memoryEntry.get())
        self.controller.difficulty = int(self.difficulty.get())
        self.controller.show_frame("MemorizePage")

    #Make sure the entry widget only accepts numbers as input
    def validate(self, action, index, value_if_allowed, prior_alue, text,
                 validation_type, trigger_type, widget_name):
        if text in "0123456789":
            try:
                int(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

class MemorizePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        
        #Grid Configurment
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.grid_columnconfigure(0, weight=1)
        #self.grid_columnconfigure(1, weight=1)

        #Listbox
        self.itemScrollbar = ttk.Scrollbar(self)
        self.itemScrollbar.grid(row=0, column=1, sticky="NSEW")

        self.itemListbox = tk.Listbox(self, yscrollcommand=self.itemScrollbar.set)
        self.itemListbox.grid(row=0, column=0, sticky="NSEW")
        self.itemScrollbar.config(command=self.itemListbox.yview)
        
        #Start Recalling Button
        self.startButton = ttk.Button(self, text="Start Recall",
                            command=lambda: self.start())
        self.startButton.grid(row=1, column=0, columnspan=2, sticky="NSEW", pady=5)


    def when_raised(self):
        #Determine items to memorize
        size = 0
        size = sum(1 for line in open("words.txt"))

        print (self.controller.number_of_items)
        for i in range(0, self.controller.number_of_items):
            x = random.randint(0, size-1)
            self.controller.selection.append(linecache.getline("words.txt", x))   

        peg_number = 0
        for i in self.controller.selection:
            peg_number += 1
            self.itemListbox.insert(peg_number, str(peg_number) + ". " + i)

    def start(self):
        self.controller.show_frame("RecallPage")

class RecallPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller

        self.shuffled_selection = []
        self.current_word = ""
        self.current_peg = 0

        self.revealButton = ttk.Button(self, text="Reveal Answer",
                            command=lambda: self.reveal())

        self.yesButton = ttk.Button(self, text="Yes",
                            command=lambda: self.yes())
        self.noButton = ttk.Button(self, text="No",
                            command=lambda: self.no())

        self.pegLabel = ttk.Label(self, text="")
        self.pegLabel.grid(row=0, column=0, columnspan=2, sticky="NSEW", pady=5)

        self.wordLabel = ttk.Label(self, text="")
        self.wordLabel.grid(row=1, column=0, columnspan=2, sticky="NSEW", pady=5)

    def when_raised(self):
        self.shuffled_selection = list(self.controller.selection)
        random.shuffle(self.shuffled_selection)
        
        self.next_word()
        self.revealButton.grid(row=2, column=0, columnspan=2, sticky="NSEW", pady=5)

    def reveal(self):
        self.revealButton.grid_forget()
        self.yesButton.grid(row=2, column=0, sticky="NSEW", pady=5)
        self.noButton.grid(row=2, column=1, sticky="NSEW", pady=5)

        self.wordLabel.config(text=self.current_word)

    def yes(self):
        self.revealButton.grid(row=2, column=0, columnspan=2, sticky="NSEW", pady=5)
        self.yesButton.grid_forget()
        self.noButton.grid_forget()

        self.controller.number_correct += 1
        self.next_word()

    def no(self):
        self.revealButton.grid(row=2, column=0, columnspan=2, sticky="NSEW", pady=5)
        self.yesButton.grid_forget()
        self.noButton.grid_forget()
        self.next_word()

    def next_word(self):
        if len(self.shuffled_selection) == 0:
            self.controller.show_frame("ResultsPage")
        else:
            self.current_word = self.shuffled_selection.pop()
        
            for i, j in enumerate(self.controller.selection):
                if j == self.current_word:
                    self.current_peg = i + 1
                
            self.pegLabel.config(text=self.current_peg)
            self.wordLabel.config(text="???")

class ResultsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        
        self.resultLabel = ttk.Label(self, text = "")
        self.resultLabel.grid(row=0, column=0, columnspan=2, sticky="NSEW", pady=5)

        #Return to start page
        self.startButton = ttk.Button(self, text="Start a New List!",
                            command=lambda: self.go_home())
        self.startButton.grid(row=1, column=0, columnspan=2, sticky="NSEW", pady=5)

    def when_raised(self):
        self.result_score = self.controller.number_correct
        self.max_score = len(self.controller.selection)

        self.resultLabel.config(text="You score is: " +
                                   str(self.result_score) + "/" + str(self.max_score))

    def go_home(self):
        self.controller.selection = []
        self.controller.number_of_items = 10
        self.controller.difficulty = 1
        self.controller.number_correct = 0

        self.controller.show_frame("StartPage")

if __name__ == "__main__":
    app = MnemonicPegSystemApp()
    app.mainloop()
    #quit()
