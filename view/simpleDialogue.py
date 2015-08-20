__author__ = 'abo.biglarpour'

from Tkinter import *

class SimpleDialogue(Toplevel):

    def __init__(self, parent, callback=None, close=None):
        """
        Simple dialogue window with
        :param parent: parent object to current window
        :param callback: A method to call back for when return clicked
                              on password field or login button pressed
        :param close: close call back
        """
        Toplevel.__init__(self, parent)
        self.transient(parent)
        self.callback = callback
        self.close = close
        self.parent = parent


    def initUi(self, title):
        """
        initialize ui elemnts
        :param title: window title
        """
        self.title(title)
        self.bodyF = Frame(self)
        self.initial_focus = self.body(self.bodyF)
        self.bodyF.pack(padx=5, pady=5)
        self.buttonbox()
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.geometry("+%d+%d" % (self.parent.winfo_rootx()+50,
                                  self.parent.winfo_rooty()+50))
        self.initial_focus.focus_set()
        self.wait_window(self)

    def body(self, master):
        """
        Need to implement main body
        """
        pass

    def buttonbox(self):
        """
        add standard button box with ok, and cancel
        """
        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.success, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.close)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.success)
        self.bind("<Escape>", self.close)

        box.pack()

    def success(self, event=None):
        """
        ok button event catcher
        """
        if not self.validate():
            self.initial_focus.focus_set()
            return

        self.withdraw()
        self.update_idletasks()
        if self.callback:
            self.callback()

        self.cancel()

    def cancel(self, event=None):
        """
        close window and put focus back to the parent window
        """
        self.destroy()

    def validate(self):
        """
        Validate that values are correct
        :return: boolean
        """
        return True