#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
from connect import connect

def definition(scheme):
    cnx = connect('root', 'mysqlpassword', 'localhost', 'worklist')
    cursor = cnx.cursor()
    request = ("SELECT definition from `schema` where `scheme`= %s")
    cursor.execute(request,(scheme,))
    definition = cursor.fetchall()[0]
    definition = definition[0].encode('utf8')
    print '\n', definition
