#!/usr/bin/python3
import json
import argparse

# Creates a course-data coding (JSON) from plain text input

def parse_course_data_from_file(f):
	# Tail-recursionesque ideas for the win.
	courses = []
	for line in f:
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
		
		#Creating Dictionary for Weekday conversion
		weekdays = {
			'monday':0,
			'montag':0,
			'mo':0,
			'mon':0,
			'tuesday':1,
			'dienstag':1,
			'tu':1,
			'di':1,
			'tue':1,
			'wednesday':2,
			'mittwoch':2,
			'we':2,
			'mi':2,
			'wed':2,
			'thursday':3,
			'donnerstag':3,
			'do':3,
			'th':3,
			'thu':3,
			'friday':4,
			'freitag':4,
			'fr':4,
			'fri':4
			}
		
		#Handle cases with illegal weekdays
		if not exercise[0].lower() in weekdays: 
			raise Exception("Weekday '" + exercise[0] + "' is not valid")
		else:
			weekday = weekdays[exercise[0].lower()]
		
		courses[-1]["tutors"][-1]["exercises"].append(
			{"day": weekday, "time": int(exercise[1].strip()[:1]), "place": exercise[2].strip()})
	f.close()
	
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
	for f in filelist:
		courses.extend(parse_course_data_from_file(f))
	return prettyprint_json(courses)

def prettyprint_json(data):
	return json.dumps(data, indent=4, sort_keys=True)

if __name__ == '__main__':
	# CLI argument parsing
	parser = argparse.ArgumentParser(
		description="Create JSON coding for courses from plain text files.")
	parser.add_argument('inputfiles', nargs='+', type=argparse.FileType('r'), metavar="inputfile", help="plain text data file(s)")
	parser.add_argument("-o", "--output", type=argparse.FileType('w'), nargs=1, help="JSON file the output is to be stored in")
	
	args = parser.parse_args()
	
	json_coding = course_file_list_to_json(args.inputfiles)
	
	if not args.output:
		print(json_coding)
	else:
		args.output[0].write(json_coding)
		args.output[0].close()
