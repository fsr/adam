#!usr/bin/python

import json
import argparse

#returns the max value of all the answer numbers in one answers list, returns -1 if there is no answer
def max_number(answers):

	maxNumber = -1 
	for answer in answers:
		if answer["number"] > maxNumber:
			maxNumber = answer["number"]

	return maxNumber

#returns the sum of all numbers in one answers list
def sum_numbers(answers):

	sumNumbers = 0
	for answer in answers:
		sumNumbers += answer["number"]

	return sumNumbers

def create_blank_bardiagram(height,width):
	#TODO: Implementation
	return 0

def y_axis_label(maxValue,numberOfValues,height,width):
	#TODO: Implementation
	return 0

def x_axis_label(answers,height,width): 
	#TODO: Implementation
	return 0

def create_bars(answers,height,width):
	#TODO: Implementation
	return 0

def create_bardiagram(question,height,width):
	#TODO: Implementation
	return 0
	


def create_report_pdf(reportJSON,outputfile):
	#TODO: Implementation
	return 0

	
		

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="Takes a report.json and builds a .svg")
	parser.add_argument("-i","--input", nargs=1, help="The report.json inputfile", required=True)
	parser.add_argument("-o","--output", nargs=1, help="The output .html file", required=True)

	args = parser.parse_args()

	create_report_pdf(args.input[0],args.output[0])
