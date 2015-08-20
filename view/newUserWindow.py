__author__ = 'abo.biglarpour'

from Tkinter import *
import simpleDialogue

class NewUserWindow(simpleDialogue.SimpleDialogue):
    _newUserFields = ["Firstname", "Lastname", "Username", 'Password']

    def body(self, master):
        """
        Add user info fields to be filled out by user for new account
        :return: first name entry object
        """
        Label(master, text="First name").grid(row=0)
        Label(master, text="Last name").grid(row=1)
        Label(master, text="Username").grid(row=2)
        Label(master, text="Passwords").grid(row=3)

        self.firstname = Entry(master)
        self.lastname = Entry(master)
        self.username = Entry(master)
        self.password = Entry(master, show="*")

        self.firstname.grid(row=0, column=1)
        self.firstname.focus()
        self.lastname.grid(row=1, column=1)
        self.username.grid(row=2, column=1)
        self.password.grid(row=3, column=1)


        self.bind("<Return>", self.success)
        self.bind("<Escape>", self.close)
        return self.username

    def success(self, event=None):
        """
        call success call back with the user inserted data
        """
        if not self.validate():
            self.initial_focus.focus_set()
            return

        self.withdraw()
        self.update_idletasks()
        if self.callback:
            userData = {"Firstname": self.firstname.get(),
                        'Lastname': self.lastname.get(),
                        'Username': self.username.get(),
                        'Password': self.password.get()}
            self.callback(userData)

        self.cancel()

