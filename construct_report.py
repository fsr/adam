#!/usr/bin/python3
import json
import argparse
import get_result
import create_coding

# Constructs a report from a report definition JSON,
# a question form definition JSON and an answer database.

# Currently reports can only be generated for one specific course.

def construct_report(reportdef, questionsdef, answersdef, dbname, coursename):
	report = []
	for definition in reportdef:
		if definition["type"] != "simple":
			raise Exception("You need an ifsr gold account to access this feature.")
		
		# Type: simple
		questionname = definition["question"]
		question = list(filter(lambda q: q["name"] == questionname, questionsdef))[0]
		questiontype = question["type"]
		
		if questiontype == "?":
			choices = question["answers"]
			# Retrieve singleresult[1] for questionname_i (i>=1) from DB
			i = 1
			answersums = []
			for answer in choices:
				singleresult = get_result.get_question(dbname, coursename, "{}_{}".format(questionname, i), definition["filter"], 1)
				answersums.append(singleresult[1])
				i += 1
			na_answer = 0
		else:
			if questiontype[-1] == "+":
				questiontype = questiontype[:-1]
				na_answer = 1
			else:
				na_answer = 0
			questionanswerdef_as_list = list(filter(lambda a: a["type"] == questiontype, answersdef))
			if len(questionanswerdef_as_list) == 0:
				raise Exception("Question type '{}' has no answers definition!".format(questiontype))
			choices = questionanswerdef_as_list[0]["answers"]
			
			# Cut away the first (answer=0 in the CSV is only for meta-questions)
			# and last (empty answer) element of the list (add later if wanted for something...)
			answersums = get_result.get_question(dbname, coursename, questionname, definition["filter"], len(choices) + na_answer)[1:-1]
		
		# Build renderable from choices and answersums
		renderable = {"question": question["text"], "view": definition["view"], "comment": definition["comment"], "answers": []}
		for i in range(len(choices)):
			renderable["answers"].append({"text": choices[i], "number": answersums[i]})
		if na_answer == 1:
			renderable["answers"].append({"text": "N/A", "number": answersums[-1]})
		report.append(renderable)
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
	parser.add_argument("-o", "--output", nargs=1, help="HTML file the report is to be stored in")
	
	args = parser.parse_args()
	
	with open(args.report[0], 'r') as f:
		reportdef = json.load(f)
	with open(args.questions[0], 'r') as f:
		questionsdef = json.load(f)
	with open(args.answers[0], 'r') as f:
		answersdef = json.load(f)
	
	report = construct_report(reportdef, questionsdef, answersdef, args.database[0], args.course[0])
	report_html = render_report_as_html(report)
	
	if not args.output:
		print(report_html)
	else:
		with open(args.output[0], 'w') as f:
			f.write(report_html)
