#!/usr/bin/python3

import sqlite3 as lite
import json

#returns the binary value of code as string
def get_binary_code(code):
	if code <= 31:
		return "{:0>5}".format(bin(code)[2:])

#returns you the whereClause you need for the sqlquery used in get_question
def create_whereString(filters):

	optionsType = {
		"eq" : "=",
		"uneq" : "!=",		#TODO: Test uneq,greater and lesser Anmerkung: Werden bei der binaeren Tutorcodierung ignoriert
		"greater" : "<",
		"lesser" : ">"
	}

	if not filters:
		return ""

	whereString = "WHERE "

	for filt in filters:

		if filt["key"] == "?code":
			bc = get_binary_code(int(filt["value"]))
			whereString += "a6={} AND b6={} AND c6={} AND d6={} AND e6={} AND ".format(bc[0],bc[1],bc[2],bc[3],bc[4])

		else:
			try:
				operatorType = optionsType[filt["type"]]
				whereString += filt["key"] + operatorType + filt["value"] + " AND " 
			except KeyError:
				print("Wrong Key for Filter {}".format(filt))
				whereString += "1=1 AND " #For the case that there is only one filter

	return whereString[:-5] #removing the last " AND "

#returns all values that belong to a question
#use filters to get a more specific query
#example call get_question(someDB.db,someTable,F1,somefilters,10)
#you will get a result with 12 values, the last one is for the empty strings
#answer value is the index in the result list!!!
def get_question(database,table,question,filters,numberoftypes):

	with lite.connect("{}".format(database)) as con:

		cur = con.cursor()

		cur.execute("SELECT {} FROM {} {};".format(question,table,create_whereString(filters)))
		values = cur.fetchall()

		result = []
		for _ in range(numberoftypes+2):
			result.append(0)

		for x, in values:
			if not x == '':
				result[x] += 1
			else:
				result[-1] += 1

		return result

def get_courses(database):
	with lite.connect("{}".format(database)) as con:
		cur = con.cursor()
		cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
		return list(map(lambda x: x[0], cur.fetchall()))
