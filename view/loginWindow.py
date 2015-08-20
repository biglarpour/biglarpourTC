__author__ = 'abo.biglarpour'

from Tkinter import *
import simpleDialogue

class LoginWindow(simpleDialogue.SimpleDialogue):

    def body(self, master):
        """
        Add username and password label and entry
        :return: username entry object
        """
        Label(master, text="Username").grid(row=0)
        Label(master, text="Password").grid(row=1)

        self.username = Entry(master)
        self.password = Entry(master, show="*")

        self.username.grid(row=0, column=1)
        self.password.grid(row=1, column=1)
        return self.username
