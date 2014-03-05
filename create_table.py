#!usr/bin/python3

import sqlite3 as lite
import sys

con = lite.connect('TestDB.db')
f = open("test_data.csv","r")
lectureName = "Vorlesung1"

header = f.readline().split(",")
header[0] = header[0].replace(" ", "")
header[-1] = header[-1].rstrip('\n')

with con:

	cur = con.cursor()
 	
 	#Name the table columns
	cur.execute("DROP TABLE IF EXISTS %s" % lectureName)
	cur.execute("CREATE TABLE %s(id INT)" % lectureName)
	for titel in header:
		cur.execute("ALTER TABLE %s ADD COLUMN %s INT" % (lectureName,titel))


	#insert values into the columns
	i = 0
	header.insert(0, "id")

	for lines in f:
		values = lines.split(",")
		values.insert(0, i)
		i = i + 1
		values[-1] = values[-1].rstrip('\n')

		cur.execute("INSERT INTO %s %s VALUES %s" % (lectureName,tuple(header),tuple(values)))
		



