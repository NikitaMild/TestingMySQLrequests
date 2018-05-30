#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import errorcode
from prettytable import from_db_cursor
from connect import connect
from INsertInTables import GetColumnName
import numpy as np

def gettable(cursor,column):
        data = cursor.fetchall()
        data = np.array(data)
        data = data.transpose()
        table = {}
        for i,j in zip(column,data):
            table[i] = j
        return table

def control(cursor,user_req,right_req, user_col, right_col):
    try:
        cursor.execute(user_req)
    except:
        return False
    user_table = gettable(cursor,user_col)
    try:
        cursor.execute(right_req)
    except:
        return False
    right_table = gettable(cursor,right_col)
    right_col = sorted(right_col)
    user_col = sorted(user_col)
    flag = True
    if right_col != user_col:
        return False
    else:
        for col in right_col:
            if np.array_equal(user_table[col],right_table[col]):
                flag = True
                continue
            else:
                flag = False
                break
        return flag


def ColNames(cursor):
        col_names = cursor.description
        column = [col_name[0] for col_name in col_names]
        return column

def DataOnTable(cursor):
        x = from_db_cursor(cursor)
        print x
        x.clear_rows()

def check(userdb, user_req, right_req,parameters,tablename):
    try:
        cnx = connect('root','mysqlpassword','localhost', userdb)
        cursor = cnx.cursor()
        cursor.execute(user_req)
    except:
        return False
    print "Your data: "
    DataOnTable(cursor)
    user_col = ColNames(cursor)
    try:
        cursor.execute(right_req)
    except:
        return False
    print "Right data: "
    DataOnTable(cursor)
    right_col = ColNames(cursor)
    flag = control(cursor,user_req,right_req,user_col,right_col)
    if flag:
        for i in xrange(1,4):
            cnx = connect('root','mysqlpassword','localhost', userdb+str(i))
            cursor = cnx.cursor()
            flag = control(cursor,user_req,right_req,user_col,right_col)
    return flag


def CheckReq(userdb,reqtype,right_req,user_req,tablename):
    cnx = connect('root','mysqlpassword','localhost','worklist')
    cursor = cnx.cursor()
    parameters = GetColumnName(cursor,userdb,tablename)
    flag = check(userdb,user_req,right_req,parameters,tablename)
    return flag
