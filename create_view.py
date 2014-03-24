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
	svgString = '<g id="diagra">'
	svgString += '<line stroke="rgb(10%,10%,16%)" x1="0" x2="{0}" y1="{1}" y2="{1}" />\n'.format(width,height*0.9)
	svgString += '<line stroke="rgb(10%,10%,16%)" x1="{0}" x2="{0}" y1="0" y2="{1}" />\n'.format(width*0.1,height)
	svgString += '<line stroke="rgb(10%,10%,16%)" x1="{0}" x2="{1}" y1="{2}" y2="{2}" />\n'.format(width*0.08,width*0.12,height*0.7)
	svgString += '<line stroke="rgb(10%,10%,16%)" x1="{0}" x2="{1}" y1="{2}" y2="{2}" />\n'.format(width*0.08,width*0.12,height*0.5)
	svgString += '<line stroke="rgb(10%,10%,16%)" x1="{0}" x2="{1}" y1="{2}" y2="{2}" />\n'.format(width*0.08,width*0.12,height*0.3)
	svgString += '<line stroke="rgb(10%,10%,16%)" x1="{0}" x2="{1}" y1="{2}" y2="{2}" />\n'.format(width*0.08,width*0.12,height*0.1)
	svgString += '</g>'
	
	return svgString

def y_axis_name(maxNumber,height,width):
	svgString = '<g id="YAxisName">'
	svgString += '<text x="{}" y="{}" textLength="{}">{}</text> \n'.format(width*0.02,height*0.7,width*0.04,maxNumber*0.25)
	svgString += '<text x="{}" y="{}" textLength="{}">{}</text> \n'.format(width*0.02,height*0.5,width*0.04,maxNumber*0.5)
	svgString += '<text x="{}" y="{}" textLength="{}">{}</text> \n'.format(width*0.02,height*0.3,width*0.04,maxNumber*0.75)
	svgString += '<text x="{}" y="{}" textLength="{}">{}</text> \n'.format(width*0.02,height*0.1,width*0.04,maxNumber)
	svgString += '</g>'

	return svgString

def x_axis_bars(answers,height,width): #TODO: Bars und Beschriftung auseinanderfummeln
	barProcent = width*(0.7 / len(answers))
	scale = (1/max_number(answers)) * (height * 0.8)
	cursor = width*0.12
	svgString = '<g id="bars">'

	for answer in answers:
		barheight = answer["number"] * scale
		svgString += '<text x="{0}" y="{1}" textLength="{2}">{3}</text> \n'.format(cursor,height*0.95,height*0.1,answer["text"])
		svgString +='<rect x="{0}" y="{1}" width="{2}" height="{3}" style="fill:rgb(0,0,139);" />\n'.format(cursor,(height*0.9)-barheight,barProcent*0.8,barheight)
		cursor += barProcent

	svgString += "</g>"
	return svgString

	

def create_bardiagram(question,height,width):
	svgString ='<svg baseProfile="tiny" height="100%" version="1.2" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs />\n'
	svgString += create_blank_bardiagram(height,width)
	svgString += y_axis_name(max_number(question["answers"]),height,width)
	svgString += x_axis_bars(question["answers"],height,width)
	svgString += '</svg>'
	return svgString
	


def create_report_svg(reportJSON,outputfile):

	with open(reportJSON) as f:

		report = json.load(f)
		i = 0
		htmlString = '<html><head><title>A report</title></head><body>'

		for question in report:
			i += 1 

			htmlString += '<div id="{}{}">\n'.format(question["view"],str(i))
			htmlString += '<h1>{}</h1>\n'.format(question["question"])
			htmlString += create_bardiagram(question,700,700)
			htmlString += '</div>\n'

		htmlString += '</body>\n</html>'
		with open(outputfile,'w') as f:
			f.write(htmlString)

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="Takes a report.json and builds a .svg")
	parser.add_argument("-i","--input", nargs=1, help="The report.json inputfile", required=True)
	parser.add_argument("-o","--output", nargs=1, help="The output .html file", required=True)

	args = parser.parse_args()


	create_report_svg(args.input[0],args.output[0])