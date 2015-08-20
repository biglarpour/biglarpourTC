__author__ = 'abo.biglarpour'

import collections

USER_TABLE = collections.OrderedDict([("userId", "INTEGER PRIMARY KEY"),
                                      ("Username", "VARCHAR NOT NULL"),
                                      ("Password", "VARCHAR NOT NULL"),
                                      ("Firstname", "VARCHAR"),
                                      ("Lastname", "VARCHAR"),
                                      ("currentRank", "VARCHAR")])

RANKS = collections.OrderedDict([("rankId", "INTEGER PRIMARY KEY"),
                                      ("rankName", "VARCHAR NOT NULL"),
                                      ("rankDescription", "VARCHAR"),
                                      ("rankCategory", "VARCHAR"),
                                      ("minTime", "VARCHAR"),
                                      ("sortNum", "INT NOT NULL")])

RANK_HISTORY = collections.OrderedDict([("rankId", "INTEGER PRIMARY KEY"),
                                        ("rankDescription", "VARCHAR")])

RANK_LIST = ['Scout',
             'Tenderfoot']
