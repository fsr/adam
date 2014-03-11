#!/usr/bin/python3
import json
import argparse
import get_result

# Constructs a report from a report definition JSON,
# a question form definition JSON and an answer database.

# Currently reports can only be generated for one specific course.

# For now it shall also include basic HTML rendering, but that is only meant to be.... temporary.

def construct_report(reportdef, questionsdef, answersdef, dbname, coursename):
	report = []
	for definition in reportdef:
		if definition["type"] != "simple":
			raise Exception("You need an ifsr gold account to access this feature.")
		
		# Type: simple
		questionname = definition["question"]
		questiontype = filter(lambda q: q["name"] == questionname, questionsdef)[0]["type"]
		choices = filter(lambda q: q["type"] == questiontype, answersdef)[0]["answers"]
		if questiontype == "?":
			raise Exception("Metaquestions are not yet supported.")
		else:
			# Cut away the first (answer=0 in the CSV is only for meta-questions)
			# and last (empty answer) element of the list
			#answersums = get_result.get_question
			# TODO, because this is a temporary commit for Simon
			pass
	return report

def render_report_as_html(report):
	return create_coding.prettyprint_json(report)

if __name__ == '__main__':
	# CLI argument parsing
	parser = argparse.ArgumentParser(
		description="Constructs a report from a report definition JSON, a question form definition JSON and an answer database.")
	parser.add_argument("-r", "--report", nargs=1, help="report definition JSON", required=True)
	parser.add_argument("-q", "--questions", nargs=1, help="question form JSON", required=True)
	parser.add_argument("-a", "--answers", nargs=1, help="answer types JSON", required=True)
	parser.add_argument("-d", "--database", nargs=1, help="database containing table with the answers...", required=True)
	parser.add_argument("-c", "--course", nargs=1, help="...for this course to generate the report on", required=True)
	parser.add_argument("-o", "--output", nargs=1, help="HTML file the report is to be stored in", required=True)
	
	args = parser.parse_args()
	
	with open(args.report[0], 'r') as f:
		reportdef = json.load(f)
	with open(args.questions[0], 'r') as f:
		questionsdefs = json.load(f)
	with open(args.answers[0], 'r') as f:
		answersdefs = json.load(f)
	
	report = construct_report(reportdef, questionsdef, answersdef, args.database[0], args.course[0])
	report_html = render_report_as_html(report)
	
	if not args.output:
		print(report_html)
	else:
		with open(args.output[0], 'w') as f:
			f.write(report_html)
