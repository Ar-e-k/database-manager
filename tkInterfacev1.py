import tkinter as tk
from tkinter import ttk

class screen:

    def __init__(self, app, buttons=None, lables=None, entries=None, order=None, choices=None):
        self.app=app
        self.lables_in=lables
        self.entries_in=entries
        self.buttons_in=buttons
        self.choices_in=choices
        self.lables={}
        self.entries={}
        self.buttons={}
        self.choices={}
        func_list=[self.lable_check, self.entry_check, self.button_check, self.choice_check]
        if order==None:
            for i in range(0, 4):
                func_list[i]()
        else:
            for i in order:
                func_list[i]()
        self.app.pack()

    def lable_check(self):
        if self.lables_in!=None:
            for lable in self.lables_in:
                self.lables[lable[0]]=self.lable(lable[0], lable[1])

    def entry_check(self):
        if self.entries_in!=None:
            for entry in self.entries_in:
                self.entries[entry[0]]=self.entry(entry[1])

    def button_check(self):
        if self.buttons_in!=None:
            for button in self.buttons_in:
                self.buttons[button[0]]=self.button(button[0], button[1], button[2])

    def choice_check(self):
        if self.choices_in!=None:
            for choice in self.choices_in:
                self.choices[choice[0]]=self.choice(choice[0], choice[1], choice[2])

    def lable(self, name, pack):
        lable=tk.Label(self.app.master)
        lable["text"]=name
        lable.pack(pack)
        return lable

    def entry(self, pack):
        entry=tk.Entry(self.app.master)
        entry.pack(pack)
        return entry

    def button(self, name, command, pack):
        button=tk.Button(self.app.master)
        button["text"]=(name)
        button["command"]=command
        button.pack(pack)
        return button

    def choice(self, name, attributes, pack):
        choice=ttk.Combobox(self.app.master, values=attributes, state="readonly")
        choice.pack(pack)
        return choice

    def get_text(self):
        texts={}
        for entry in self.entries.keys():
            texts[entry]=self.entries[entry].get()
        return texts

    def get_choice(self):
        choice={}
        for entry in self.choices.keys():
            choice[entry]=self.choices[entry].get()
        return choice

    def clear_screen(self):
        for value in self.buttons.values():
            value.destroy()
        for value in self.lables.values():
            value.destroy()
        for value in self.entries.values():
            value.destroy()
        for value in self.choices.values():
            value.destroy()
