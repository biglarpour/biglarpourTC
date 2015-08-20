__author__ = 'abo.biglarpour'

import sys
import os
import json
import time

import view.loginWindow
import view.newUserWindow
import view.homeWindow
import view.userStatusWindow
import model
import model.mySqlite


class ScoutCtrl(object):

    def __init__(self):
        """
        A simple controller for bringing the Qt windows and sqlite models together.
        """
        self.homePage      = None
        self.loginWindow   = None
        self.newUserWindow = None
        self.userStatusWindow    = None
        self.username      = ""
        self.password      = ""
        self.assetsFolder  = "%s/assets"%os.path.dirname(sys.argv[0])

        if not os.path.exists(self.assetsFolder):
            os.mkdir(self.assetsFolder)
        dbPath = "%s/scouts.db"%self.assetsFolder
        self.mySql = model.mySqlite.MySqlite(os.path.normpath(dbPath))

    def createHomePage(self):
        """
        Creates the home page, the first landing page
        """
        self.homePage = view.homeWindow.HomeWindow(loginCallback=self.createLoginWindow,
                                                   newUserCallback=self.createNewUserWindow)
        self.homePage.setBtns()
        self.homePage.root.mainloop()
        exit()

    def createLoginWindow(self):
        """
        Creates the login window to authenticate user information
        """
        self.username = ""
        self.password = ""
        self.loginWindow = view.loginWindow.LoginWindow(self.homePage.root,
                                                        callback=self.createUserStatusWindow,
                                                        close=self.closeLoginWindow)
        self.loginWindow.initUi("Login Window")

    def createNewUserWindow(self):
        """
        Creates the new user window to get information from user inorder to
        create a new data entry in the database
        """
        self.newUserWindow = view.newUserWindow.NewUserWindow(self.homePage.root,
                                                              callback=self.createNewUser,
                                                              close=self.closeNewUserWindow)
        self.newUserWindow.initUi("New User Window")
        self.homePage.hide()

    def createNewUser(self, data):
        """
        Takes the data from the new user window and inserts the user info
        into the database
        :param data: dictionary object of the user information
        """
        self.validateScoutsTable()
        if self.mySql.rowExists('scoutUsers', {'Username':data.get('Username')}):
            return self.createNewUserWindow()
        self.mySql.addValue('scoutUsers', json.dumps(data))
        self.username = data.get('Username')
        self.password = data.get('Password')
        time.sleep(1)
        self.createUserStatusWindow()

    def createUserStatusWindow(self):
        """
        Creates the user status window. Using the object username and password
        gathers all the necessary information to build the window, this includes
        getting users rank history to figure what the next steps should be
        and also user first and last name
        """
        if self.loginWindow:
            if not self.username:
                self.username = self.loginWindow.username.get()
            if not self.password:
                self.password = self.loginWindow.password.get()
        if self.userStatusWindow:
            self.userStatusWindow.cancel()

        userInfo = self.getUserInfo(self.username, self.password)
        if not userInfo:
            return
        if self.loginWindow:
            self.loginWindow.cancel()
        elif self.newUserWindow:
            self.newUserWindow.cancel()

        userId = userInfo.get('userId')
        userTable = "%s_%s"%(self.username, userId)
        rankHistory = [rank.get('rankDescription') for rank in
                       self.mySql.queryValues(userTable, "")]
        rank = userInfo.get('currentRank')
        if rank is None:
            rank = 'Scout'
        self.validateRankTable()
        rankQueryDict = {'rankName':rank}
        allRankData = self.mySql.queryValues("ranks", rankQueryDict)
        rankDataList = [rankData for rankData in allRankData
                        if not rankData.get('rankDescription').replace(u"\xa0", u" ") in rankHistory]
        if len(rankDataList) == 0:
            rank, rankDataList = self.addNextRank(rank)

        self.userStatusWindow = view.userStatusWindow.UserStatusWindow(self.homePage.root,
                                                                 userInfo,
                                                                 rank,
                                                                 rankDataList,
                                                                 saveCallback=self.saveRanks,
                                                                 refreshCallback=self.createUserStatusWindow,
                                                                 fetchCallback=self.fetchAssets,
                                                                 close=self.closeUserStatusWindow)
        self.userStatusWindow.initUi("User Status")

    def addNextRank(self, rank):
        """
        Creates the next available rank, for test purposes there are only two
        ranks available, but this method is scalable if the rank data exists.
        :param rank: the name of the current rank
        :return: a tuple first item being the next rank name and second item
                 being a list of all requirements to finish the next rank.
        """
        rankDataList = []
        allRanks = model.RANK_LIST
        nextRankIndex = allRanks.index(rank) + 1
        try:
            rank = allRanks[nextRankIndex]
        except IndexError:
            rank = None
        if rank:
            rankQueryDict = {'rankName':rank}
            rankDataList = self.mySql.queryValues("ranks", rankQueryDict)
            queryDict = {'Username':self.username}
            valueDict = {'currentRank':rank}
            self.mySql.updateRow('scoutUsers', json.dumps(queryDict), json.dumps(valueDict))
        return rank, rankDataList

    def saveRanks(self):
        """
        Saves the checked ranks that the user has completed, will remove the
        checked ranks from the current rank and add to the rank history for the current user.
        """
        userInfo = self.mySql.queryValues('scoutUsers', {'Username':self.username}, fetchone=True)
        if not userInfo:
            print "Failed to get user info"
            return
        for checkBox in self.userStatusWindow.checkBoxList:
            for k,v in checkBox.val.items():
                if v.get() == 1:
                    queryDict = {'rankDescription':k}
                    rank = self.mySql.queryValues('ranks', queryDict, fetchone=True)
                    if rank:
                        userTable = "%s_%s"%(self.username, userInfo.get('userId'))
                        rankHistoryDict = {'rankId':rank.get('rankId'),
                                           'rankDescription':k}
                        self.mySql.addValue(userTable, json.dumps(rankHistoryDict))
                        checkBox.grid_forget()

    def closeLoginWindow(self):
        """
        Closes the login window and cleans the variable
        """
        self.loginWindow.cancel()
        self.loginWindow = None

    def closeNewUserWindow(self):
        """
        Closes the new user window and cleans the variable
        """
        self.newUserWindow.cancel()
        self.newUserWindow = None

    def closeUserStatusWindow(self):
        """
        Closes the user status window and cleans the variable
        """
        self.userStatusWindow.cancel()
        self.userStatusWindow = None

    def validateScoutsTable(self):
        """
        Validate that the scoutUsers tables exists,
        if not create the table with the proper columns and foreign keys
        """
        foreignKeys = [{'key':'currentRank',
                        'refTable': 'ranks',
                        'refValue': 'rankName'}]
        self.mySql.createTable("scoutUsers", json.dumps(model.USER_TABLE), foreignKeys)

    def validateUserHistoryTable(self, tableName):
        """
        Validate that the userHistory tables exists,
        if not create the table with the proper columns and foreign keys
        :param tableName: userHistory table names use the following naming convention:
                          <username>_<userId>
        """
        foreignKeys = [{'key':'rankId',
                        'refTable': 'ranks',
                        'refValue': 'rankId'}]
        self.mySql.createTable(tableName, json.dumps(model.RANK_HISTORY), foreignKeys)

    def validateRankTable(self):
        """
        Validate that the ranks tables exists,
        if not create the table with the proper columns and foreign keys,
        it will also fetch all the rank data from a json located in the assets
        directory for test purpose and load all data into the sql database
        """
        rankData = []
        if not self.mySql.tableExists('ranks'):
            self.mySql.createTable('ranks', json.dumps(model.RANKS))
            rankDataPath = "%s/%s"%(self.assetsFolder, "rankData.json")
            with open(os.path.normpath(rankDataPath), 'r') as _file:
                rankData = json.load(_file)
            if rankData:
                for rank in rankData:
                    rankDict = {'rankName':rank['rankName'],
                                'rankDescription':rank['Rank'].replace(u"\xa0", u" "),
                                'rankCategory':rank['Category'],
                                'minTime': rank['Minimum Time'],
                                'sortNum':rank['Numerical Order']}
                    self.mySql.addValue('ranks', json.dumps(rankDict))
    #
    def getUserInfo(self, username, password):
        """
        get the user info from database, if invalid user data displace incorrect
        username or password dialogue
        :param username: current entered username
        :param password: current entered password
        :return: user info as dictionary object
        """
        self.validateScoutsTable()
        queryDict = {'Username':username, 'Password':password}
        userInfo = self.mySql.queryValues('scoutUsers', queryDict, fetchone=True)
        if userInfo:
            userTableName = "%s_%s"%(username, userInfo.get('userId'))
            self.validateUserHistoryTable(userTableName)
            return userInfo
        else:
            view.failedLoginMessage(self.createNewUserWindow)

    def fetchAssets(self):
        """
        Gets the list of items from the assets folder located in the same folder
        as the executable and displays in info message box
        """
        assetList = [_file for _file in os.listdir(self.assetsFolder)
                     if not _file.startswith(".")]
        view.showAssetsMessage(assetList, self.assetsFolder)