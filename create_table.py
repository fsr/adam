#!usr/bin/python3

import sqlite3 as lite
import argparse
import re

def create_table(lectureName, inputfile, db):

	con = lite.connect("{}".format(db))

	with open(inputfile,"r") as f:
		header = f.readline().split(",")
		header = list(map(lambda s: ''.join(s.split()), header))

		with con:

			cur = con.cursor()
			
			# Name the table columns
			cur.execute("DROP TABLE IF EXISTS {}".format(lectureName))
			types = ""
			for title in header:
				types += "{} INT, ".format(title)
			cur.execute("CREATE TABLE {}({})".format(lectureName, types[:-2]))


			# insert values into the columns
			# Note: sqlite automatically adds a (semi-hidden) ROWID column for all rows!
			for lines in f:
				values = list(map(lambda s: s.strip(), lines.split(",")))
				cur.execute("INSERT INTO {} {} VALUES {}".format(lectureName, tuple(header), tuple(values)))


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="Import .csv import into a sqllite3 database.")
	
	parser.add_argument("-d","--database", nargs=1, help="The sqllite3 db for the output", required=True)
	parser.add_argument("-i","--importfile", nargs="+" ,help="1-Many imput .csv imports", required=True)

	args = parser.parse_args()
	db = args.database[0]

	for arg in args.importfile:
		if arg.endswith(".CSV"):
			name = re.sub('[\W_]+','',arg) # removes all the none alphanumeric chars from the string
			create_table(name,arg,db)