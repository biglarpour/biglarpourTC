__author__ = "abo.biglarpour"

import simpleDialogue
from Tkinter import *
import ttk

class UserStatusWindow(simpleDialogue.SimpleDialogue):
    def __init__(self, parent, userInfo, rank, rankDataList, saveCallback=None,
                 refreshCallback=None, fetchCallback=None, close=None):
        """
        :param userInfo: user info dictionary from database
        :param rank: string rank name
        :param rankDataList: list of all remaining requirements to finish task
        :param saveCallback: save method call back
        :param refreshCallback: call back for refresh button
        :param fetchCallback: call back for fetching assets items
        """
        simpleDialogue.SimpleDialogue.__init__(self, parent, saveCallback, close)
        self.saveCallback = saveCallback
        self.refreshCallback = refreshCallback
        self.fetchCallback = fetchCallback
        self.close = close
        self.userInfo = userInfo
        self.rank = rank
        self.rankDataList = rankDataList
        self.checkBoxList = []

    def buttonbox(self):
        """
        Add buttons for user status window including:
        save button, reload button, show assets button, and exit button.
        """
        box = Frame(self)
        saveButton = Button(box, text="Save", width=10, command=self.saveCallback, default=ACTIVE)
        saveButton.pack(side=LEFT, padx=5, pady=5)
        refreshButton = Button(box, text="Reload", width=10, command=self.refreshCallback)
        refreshButton.pack(side=LEFT, padx=5, pady=5)
        fetchButton = Button(box, text="Show assets", width=10, command=self.fetchCallback)
        fetchButton.pack(side=LEFT, padx=5, pady=5)
        closeButton = Button(box, text="Exit", width=10, command=self.close)
        closeButton.pack(side=LEFT, padx=5, pady=5)
        box.pack()

    def body(self, master):
        """
        Add user info data as labels and all rank data as checkboxes
        to complete and save
        """
        Label(master, text="Hi %(Firstname)s %(Lastname)s!"%self.userInfo,
              anchor=W, justify=LEFT).grid(row=0, sticky=W)
        Label(master, text="Your current rank is %s"%self.rank, anchor=W,
              justify=LEFT).grid(row=1, sticky=W)
        ttk.Separator(master, orient=HORIZONTAL).grid(row=2, columnspan=5,
                                                      sticky="ew")
        for index, rankItem in enumerate(self.rankDataList):
            index += 3
            var = IntVar()
            checkbox = Checkbutton(master,text=rankItem.get('rankDescription'),
                                   variable=var)
            checkbox.grid(row=index, sticky=W)
            checkbox.val = {rankItem.get('rankDescription'):var}
            self.checkBoxList.append(checkbox)
