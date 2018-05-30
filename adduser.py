#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mysql
import mysql.connector

try:
    cnx = mysql.connector.connect(user='root', password='mysqlpassword',
                                  host='localhost')
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
    
username = raw_input("please, enter your username: ")
userpass = raw_input("please, enter your password: ")
userhost = raw_input("please, enter your host: ")

cursor = cnx.cursor()
adduser = ('CREATE USER %s@%s IDENTIFIED BY %s')

user_information = (username, userhost, userpass)
cursor.execute(adduser,user_information)
cnx.commit()
cursor.close()
cnx.close()
