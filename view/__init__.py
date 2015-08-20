__author__ = 'abo.biglarpour'

import os
import tkMessageBox



def failedLoginMessage(callback=""):
    """
    Warns user about invalid username or password and ask if user wants
    to create a new account.
    :param callback: call back for launching new user window
    """
    title = "Incorrect login"
    message = "The username or password is incorrect.\n" \
              "Would you like to create a new account?"
    msgBox = tkMessageBox.askquestion(title, message)
    if msgBox == 'yes':
        if callback:
            callback()
    else:
        print  "Canceled"

def showAssetsMessage(assetsList, path):
    """
    Show all assets from the assets folder in info message box
    :param assetsList: list of items in assets folder
    :param path: path to the assets folder
    """
    title =  os.path.normpath(path)
    message = "Found %d asset files:\n"%len(assetsList)
    message += "\n".join(assetsList)
    msgBox = tkMessageBox.showinfo(title, message)
    if msgBox == 'yes':
        pass
    else:
        pass