#!/usr/bin/python3
import json
import argparse

# Exports course-data coding (JSON) into various usable and readable formats

def decimal_to_binary(number):
	outstring = ""
	if number > 31:
		raise Exception("Coding number is too high ({}>31)!".format(number))
	if number >= 16:
		outstring += "1"

def print_as_plaintext(coursedata):
	output = ""
	# coursedata can contain multiple courses or just one
	for course in coursedata:
		output += "{} ({})\n".format(course["name"], course["lecturer"])
		for tutor in course["tutors"]:
			output += "\t{}\t{} {}\n".format(tutor["code"], tutor["firstname"], tutor["lastname"])
	return output

def print_as_html(coursedata, cssfile):
	output = "<html>\n<head><title>EVA tutor coding slides</title>"
	output += "<link type=\"text/css\" rel=\"stylesheet\" href=\"{}\" /></head>\n<body>\n".format(cssfile)
	# coursedata can contain multiple courses or just one
	for course in coursedata:
		output += "<h1>{}</h1><h2>{}</h2>\n<table style=\"page-break-after:always\">\n".format(course["name"], course["lecturer"])
		output += "<tr><th>Exercise</th><th>Tutor</th>"
		for i in [16,8,4,2,1]:
			output += "<th class=\"codingcell\"><small>{}</small></th>".format(i)
		output += "</tr>\n"
		for tutor in course["tutors"]:
			for exercise in tutor["exercises"]:
				extext = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"][exercise["day"]]
				extext += ", {}. DS, {}".format(exercise["time"], exercise["place"])
				codecells = "";
				for char in "{:0>5}".format(bin(tutor["code"])[2:]):
					if char == "0": filledclass = "notfilled"
					else: filledclass = "filled"
					codecells += "<td class=\"codingcell {}\"></td>".format(filledclass)
				output += "<tr><td>{}</td><td>{} {}</td>{}</tr>\n".format(
					extext, tutor["firstname"], tutor["lastname"], codecells)
		output += "</table>\n"
	return output + "</body>\n</html>"

if __name__ == '__main__':
	# CLI argument parsing
	parser = argparse.ArgumentParser(
		description="Export course data JSON coding into formatted output (slides etc.).")
	subparsers = parser.add_subparsers(dest='type',
		help="output type")
	
	parser_plain = subparsers.add_parser("plain")
	
	parser_html = subparsers.add_parser("html")
	parser_html.add_argument("-s", "--stylesheet", nargs=1, help="stylesheet to link to", required=True);
	
	parser.add_argument('inputfile', nargs=1, type=argparse.FileType('r'), help="JSON data file")
	
	# Add this twice now for more reasonable argument order
	parser_plain.add_argument("-o", "--output", type=argparse.FileType('w'), nargs=1, help="file the output is to be stored in")
	parser_html.add_argument("-o", "--output", type=argparse.FileType('w'), nargs=1, help="file the output is to be stored in")
	
	args = parser.parse_args()
	
	json_coding = json.load(args.inputfile[0])
	args.inputfile[0].close()
	
	if args.type == "plain":
		outtext = print_as_plaintext(json_coding)
	else:
		outtext = print_as_html(json_coding, args.stylesheet[0])
	
	if not args.output:
		print(outtext)
	else:
		args.output[0].write(outtext)
		args.output[0].close()
