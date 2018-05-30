#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import errorcode
import getpass
from connect import connect

def create_db(cursor,DB_NAME):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


if __name__ == '__main__':
    username = raw_input("please, enter your username: ")
    userpass = getpass.getpass("PLease, enter your password: ")
    userhost = raw_input("please, enter your host: ")

    cnx = connect(username,userpass,userhost,"None")
    try:
        cursor = cnx.cursor()
        DB_NAME = raw_input("Enter DB name which you want create: ")
        cnx.database = DB_NAME
        print("{}: This database already was created ".format(DB_NAME))
        cursor.close()
        cnx.close()
        exit(0)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_db(cursor,DB_NAME)
            cursor.close()
            cnx.close()
            exit(0)
        else:
            print(err)
            cursor.close()
            cnx.close()
            exit(1)
