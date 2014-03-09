#!usr/bin/python3

import sqlite3 as lite
import argparse
import re
import os

def create_table(tableName, inputfile, db):

	with open(inputfile,"r") as f:
		header = f.readline().split(",")
		header = list(map(lambda s: ''.join(s.split()), header))

		with lite.connect("{}".format(db)) as con:

			cur = con.cursor()
			
			# Name the table columns
			cur.execute("DROP TABLE IF EXISTS {}".format(tableName))
			types = ""
			for title in header:
				types += "{} INT, ".format(title)
			cur.execute("CREATE TABLE {}({})".format(tableName, types[:-2]))


			# insert values into the columns
			# Note: sqlite automatically adds a (semi-hidden) ROWID column for all rows!
			for lines in f:
				values = list(map(lambda s: s.strip(), lines.split(",")))
				cur.execute("INSERT INTO {} {} VALUES {}".format(tableName, tuple(header), tuple(values)))

#walks a specified directory and inserts als .csv files into a database
def insert_directory(directory,database):
	for root,dirs,files in os.walk(directory):
		for fil in files:
			if fil.endswith(".CSV"):
				filePath = "{}\{}".format(root,fil)
				tableName = re.sub('[\W_]+','',fil)
				create_table(tableName, filePath, database)


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="Import .csv import into a sqllite3 database.")
	subparser = parser.add_subparsers(dest="type")

	parser_directory = subparser.add_parser("dir")
	parser_files =  subparser.add_parser("file")

	parser.add_argument("-d","--database", nargs=1, help="The sqllite3 db for the output", required=True)
	
	parser_directory.add_argument("directory", nargs=1, help="One input directory")
	parser_files.add_argument("importfile", nargs="+" ,help="1-Many imput .csv imports")

	args = parser.parse_args()
	db = args.database[0]

if args.type == "file":
	for arg in args.importfile:
		tableName = re.sub('[\W_]+','',arg) # removes all the none alphanumeric chars from the string
		create_table(tableName,arg,db)
else:
	insert_directory(args.directory[0],db)
