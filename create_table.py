#!usr/bin/python3

import sqlite3 as lite
import sys

con = lite.connect('TestDB.db')
f = open("real_files/test_data.csv","r")
lectureName = "Vorlesung1"

header = f.readline().split(",")
header = list(map(lambda s: ''.join(s.split()), header))

with con:

	cur = con.cursor()
 	
 	# Name the table columns
	cur.execute("DROP TABLE IF EXISTS %s" % lectureName)
	types = ""
	for title in header:
		types += "%s INT, " % title
	cur.execute("CREATE TABLE %s(%s)" % (lectureName, types[:-2]))


	# insert values into the columns
	# Note: sqlite automatically adds a (semi-hidden) ROWID column for all rows!
	for lines in f:
		values = list(map(lambda s: s.strip(), lines.split(",")))
		cur.execute("INSERT INTO %s %s VALUES %s" %
			(lectureName, tuple(header), tuple(values)))
