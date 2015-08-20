__author__ = 'abo.biglarpour'

from Tkinter  import *


class HomeWindow(object):
    def __init__(self, loginCallback=None, newUserCallback=None):
        """
        Simple login window
        :param loginCallback: A method to call back for when login button pressed
        :param newUserCallback: A method to call back for when new user button pressed
        """
        self.root = Tk()
        self.center()
        self.root.lift()
        self.root.title("Welcome Scouts!")
        self.root.call('wm', 'attributes', '.', '-topmost', True)
        self.root.after_idle(self.root.call, 'wm', 'attributes', '.', '-topmost', False)
        self.loginCallback = loginCallback
        self.newUserCallback = newUserCallback

    def center(self):
        """
        Center the home page to the center of screen
        """
        self.root.update_idletasks()
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        size = tuple(int(_) for _ in self.root.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        self.root.geometry("240x80+%d+%d" % (x, y))

    def setBtns(self):
        """
        Creates the login and new user button
        """
        w = Button(self.root, text="Login", width=10, command=self.loginCallback, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(self.root, text="New User", width=10, command=self.newUserCallback)
        w.pack(side=LEFT, padx=5, pady=5)
        self.root.wait_window()

    def hide(self):
        """
        hide the home page
        """
        self.root.withdraw()

    def reveal(self):
        """
        reveal the home page from hiding
        """
        self.root.deiconify()
