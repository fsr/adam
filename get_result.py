#!/usr/bin/python3

import sqlite3 as lite

#returns the binary value of code as string
def get_binary_code(code):
	if code <= 31:
		return "{:0>5}".format(bin(code)[2:])

#returns you the whereClause you need for the sqlquery used in get_question
def create_whereString(filters):
			bc = get_binary_code(filters)
			whereString = "a6={} AND b6={} AND c6={} AND d6={} AND e6={}".format(bc[0],bc[1],bc[2],bc[3],bc[4])
		

		return whereString

#returns all values that belong to a question
#use whereString to add more parameters to the sqlquery
#example call get_question(someDB.db,someTable,F1,create_whereString(..),10)
#you will get a result with 12 values, the last one is for the empty strings
#answer value is the index in the result list!!!
def get_question(database,table,question,whereString,numberoftypes):

	with lite.connect("{}".format(database)) as con:

		cur = con.cursor()

		cur.execute("SELECT {} From {} WHERE {}".format(question,table,whereString))
		values = cur.fetchall()

		result = []
		for _ in range(numberoftypes+2):
			result.append(0)

		for x, in values:
			if not x == '':
				result[x] += 1
			else:
				result[types] += 1

		return result
