#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
from TakeTask import *
from db_definition import definition
from kerner import *

if __name__ == '__main__':
    answer = "yes"
    while answer == "yes":
        reqtype = raw_input("please, enter the request type: ")
        numbtask = raw_input("please, enter the task number: ")
        data = TakeTask(reqtype,numbtask)
        if data == 0:
            exit("Your request type or task number is incorrect, try again later")
        task = data[0]
        dbname = data[1]
        right_req = data[2]
        tablename = data[3]
        definition(dbname)
        print "Задание: "
        print task
        user_req = raw_input("please, input your request: ")
        flag = CheckReq(dbname,reqtype,right_req,user_req,tablename)
        if flag == True:
            answer = raw_input("Your request is correct. You want to choose a new task? (Yes/No): ").lower()
        else:
            while answer == "yes":
                answer = raw_input("Your request is incorrect. Try again? (Yes/No): ").lower()
                if answer == "no":
                    break
                user_req = raw_input("please, input your request: ")
                flag = CheckReq(dbname,reqtype,right_req,user_req, tablename)
                if flag == True:
                    answer = raw_input("Your request is correct. You want to choose a new task? (Yes/No): ").lower()
                    break
                else:
                    continue
    if answer == "no":
        print "Good buy. See you again later!"
