#!/usr/bin/python3
import json
import argparse

def parse_questions_from_file(filename):
	questions = ["foo"]
	
	return questions

def parse_course_data_from_file(filename):
	# Tail-recursionesque ideas for the win.
	courses = []
	with open(filename, "r") as course_file:
		for line in course_file:
			# Remove newline at the end
			line = line[:-1]
			# Filter comments
			if line.startswith("#") or not line:
				continue
				
			# New course has started, start new course block
			if not line.startswith("\t"):
				course_name = (line[::-1].split("(", 1))[1][::-1].strip()
				course_lect = (line[::-1].split("(", 1))[0][:0:-1].strip()
				courses.append({"name": course_name, "lecturer": course_lect, "tutors": []})
				continue
				
			# So we have at least one indentation level, trim it:
			line = line[1:]
			# New tutor starts
			if not line.startswith("\t"):
				reversed_name_array = line[::-1].split(" ", 1)
				if len(reversed_name_array) == 1:
					first = ""
					last = line
				else:
					first = reversed_name_array[1][::-1].strip()
					last  = reversed_name_array[0][::-1].strip()
				courses[-1]["tutors"].append({"firstname": first, "lastname": last, "exercises": []})
				continue
			
			# Two tabs or more means we have to parse exercises
			exercise = line.strip().split(",",-1)
			if len(exercise) != 3: raise Exception("Line '" + line + "'is not a valid exercise")
			
			if   exercise[0] in ["Monday",    "Montag",     "Mo", "Mo", "Mon"]: weekday = 0
			elif exercise[0] in ["Tuesday",   "Dienstag",   "Tu", "Di", "Tue"]: weekday = 1
			elif exercise[0] in ["Wednesday", "Mittwoch",   "We", "Mi", "Wed"]: weekday = 2
			elif exercise[0] in ["Thursday",  "Donnerstag", "Th", "Do", "Thu"]: weekday = 3
			elif exercise[0] in ["Friday",    "Freitag",    "Fr", "Fr", "Fri"]: weekday = 4
			else: raise Exception("Weekday '" + exercise[0] + "' is not valid")
			
			courses[-1]["tutors"][-1]["exercises"].append(
				{"day": weekday, "time": int(exercise[1].strip()[:1]), "place": exercise[2].strip()})
	
	# Gonna use this soon.
	def exercise_timevalue(e):
		return e["day"]*24 + e["time"] # 24 is rather arbitrary
				
	for course in courses:
		# With everything read, sort everything starting with individual exercises per tutor...
		for tutor in course["tutors"]:
			tutor["exercises"].sort(key=exercise_timevalue)
		# ...to continue sorting the tutors accordingly
		course["tutors"].sort(key=lambda t: exercise_timevalue(t["exercises"][0]))
		# Then generate codes for tutors
		code = 1
		for tutor in course["tutors"]:
			tutor["code"] = code
			code += 1
			
	return courses

def course_file_list_to_json(filelist):
	courses = []
	for fn in filelist:
		courses.extend(parse_course_data_from_file(fn))
	return prettyprint_json(courses)

def prettyprint_json(data):
	return json.dumps(data, indent=4, sort_keys=True)

if __name__ == '__main__':
	# CLI argument parsing
	parser = argparse.ArgumentParser(
		description="Create JSON coding for courses (or optionally questions) from plain text files.")
	parser.add_argument("-t", "--type", choices=["courses", "questions"],
		default="courses", help="data that is to be parsed (default: courses)")
	parser.add_argument('inputfiles', nargs='+', metavar="inputfile", help="plain text data file(s)")
	parser.add_argument("-o", "--output", nargs=1, help="JSON file the output is to be stored in")
	
	args = parser.parse_args()
	
	if args.type == "questions":
		json_coding = prettyprint_json(parse_questions_from_file((args.inputfiles)))
	else:
		json_coding = course_file_list_to_json(args.inputfiles)
	
	if not args.output:
		print(json_coding)
	else:
		with open(args.output[0], 'w') as f:
			f.write(json_coding)
