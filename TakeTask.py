#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
import getpass
from mysql.connector import errorcode
from connect import connect

def Take(cursor,reqtype, numbtask):
    query = ("SELECT task, scheme, `correct request`, `table name` FROM worklist WHERE `request type` = %s AND `number` = %s")
    cursor.execute(query,(reqtype,numbtask))
    result = cursor.fetchall()
    return result


def TakeTask(request_type,numb_task):
    cnx = connect('root', 'mysqlpassword', 'localhost', 'worklist')
    cursor = cnx.cursor()
    storage = Take(cursor,request_type,numb_task)
    if (len(storage) == 0):
        #print("data does not exist")
        result = 0
    else:
        task = storage[0][0]
        scheme = storage[0][1]
        correq = storage[0][2]
        tablename = storage[0][3]
        result = (task, scheme, correq, tablename)
    return result
