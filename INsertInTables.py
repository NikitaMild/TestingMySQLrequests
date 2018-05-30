#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
import getpass
from mysql.connector import errorcode
import random
from connect import connect

def GetColumnName(cursor,userdb, usertable):
    get_column_name = ('''SELECT column_name FROM information_schema.columns
                          WHERE table_schema = %s
                          AND table_name = %s ''')
    cursor.execute(get_column_name, (userdb,usertable))
    parameters = cursor.fetchall()
    return parameters


def insertinf(parameters,usertable, flag, check):
    atributes = []
    if flag == 1:
        for parameter in parameters:
            temp = raw_input("please enter {}: ".format(parameter[0]))
            atributes.append(temp)
    if flag == 0:
        size = len(parameters)
        for i in xrange(size):
            atributes.append(random.choice(check[i][0])[0])
    tempstring = "("
    bracket = ")"
    backtick = "`"
    comma = ","
    for parameter in parameters:
        if parameter == parameters[-1]:
            tempstring = tempstring + backtick + parameter[-1] + backtick + bracket
            break;
        tempstring = tempstring + backtick + parameter[0] + backtick + comma

    in_p = ', '.join(['%s'] * len(atributes))
    add_information = ('''INSERT INTO `{0}`
                       {1}
                        VALUES ({2})'''.format(usertable, tempstring, in_p))
    kek = tuple(atributes)
    try:
        cursor.execute(add_information, kek)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_NO_SUCH_TABLE:
            print("Such a table does not exist")
            cursor.close()
            cnx.close()
            exit(1)
        elif err.errno == errorcode.ER_DATA_TOO_LONG:
            print("Your value is long")
            cursor.close()
            cnx.close()
            exit(1)
        elif err.errno == errorcode.ER_TRUNCATED_WRONG_VALUE_FOR_FIELD:
            print("Your value is incorrect")
            cursor.close()
            cnx.close()
            exit(1)
        elif err.errno == errorcode.WARN_DATA_TRUNCATED:
            print("your data is trancated")
            cursor.close()
            cnx.close()
            exit(1)
        elif err.errno == errorcode.ER_DUP_ENTRY:
            print("duplicate entry for key 'PRIMARY'")
            return
        else:
            print(err)
            cursor.close()
            cnx.close()
            exit(1)
    return


if __name__ == '__main__':
    username = raw_input("please, enter your username: ")
    userpass = getpass.getpass("PLease, enter your password: ")
    userhost = raw_input("please, enter your host: ")

    check = []
    auto = raw_input("do you want to fill databases with random values? (Yes/No) ").lower()
    if auto == "yes":
        the_first_db = raw_input("please enter the first databases, where you store data: ")
        the_first_user_table = raw_input("please enter table name, where you store data: ")
        cnx = connect(username,userpass,userhost,the_first_db)
        cursor = cnx.cursor(buffered=True)
        parameters = GetColumnName(cursor,the_first_db,the_first_user_table)
        reqq = ""
        n = 0
        for parameter in parameters:
            n += 1
            if parameter == parameters[-1]:
                reqq = reqq + "SELECT {0} FROM {1}".format(parameter[0], the_first_user_table)
            else:
                reqq = reqq + "SELECT {0} FROM {1}".format(parameter[0], the_first_user_table) + "; "
        check = [0] * n
        for i in range(n):
            check[i] = [0]
        j = 0
        for result in cursor.execute(reqq, multi=True):
            check[j][0] = result.fetchall()
            j+=1
        cursor.close()
        cnx.close()
        new_db = raw_input("please, enter the db which you want insert data: ")
        new_table = raw_input("please, enter the table which you want insert data: ")
        cnx = connect(username,userpass,userhost,new_db)
        cursor = cnx.cursor()
        number = int(raw_input("How many data you want insert? "))
        for i in xrange(number):
            insertinf(parameters,new_table,0,check)
            cnx.commit()
        cursor.close()
        cnx.close()
    else:
        userdb = raw_input("please choose database where store your table: ")
        cnx = connect(username,userpass,userhost,userdb)
        cursor = cnx.cursor()
        usertable = raw_input("please enter table name to which you want insert data: ")
        parameters = GetColumnName(cursor,userdb,usertable)
        answer = "yes"
        while answer == "yes":
            insertinf(parameters,usertable,1, check)
            cnx.commit()
            answer = raw_input("you still want to enter data? (Yes/No) ").lower()
        cursor.close()
        cnx.close()
