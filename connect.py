#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import errorcode


def connect(username,userpass,userhost,userdb):
    if userdb == "None":
        try:
            cnx = mysql.connector.connect(user = username, password = userpass,
                                          host = userhost)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
                exit(1)
            elif err.errno == errorcode.CR_CONN_HOST_ERROR:
                print("Host is incorrect")
                exit(1)
            else:
                print(err)
                exit(1)
        return cnx
    else:
        try:
            cnx = mysql.connector.connect(user = username, password = userpass,
                                          host = userhost,
                                          database = userdb)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
                exit(1)
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                exit(1)
            elif err.errno == errorcode.CR_CONN_HOST_ERROR:
                print("Host is incorrect")
                exit(1)
            else:
                print(err)
                exit(1)
        return cnx
