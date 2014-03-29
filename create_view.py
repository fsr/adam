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
	svg = '<g id="diagram">'
	svg += '<line stroke="rgb(10%,10%,16%)" x1="0" x2="{0}" y1="{1}" y2="{1}" />\n'.format(width,height*0.9)
	svg += '<line stroke="rgb(10%,10%,16%)" x1="{0}" x2="{0}" y1="0" y2="{1}" />\n'.format(width*0.1,height)
	svg += '<line stroke="rgb(10%,10%,16%)" x1="{0}" x2="{1}" y1="{2}" y2="{2}" />\n'.format(width*0.09,width*0.11,height*0.7)
	svg += '<line stroke="rgb(10%,10%,16%)" x1="{0}" x2="{1}" y1="{2}" y2="{2}" />\n'.format(width*0.09,width*0.11,height*0.5)
	svg += '<line stroke="rgb(10%,10%,16%)" x1="{0}" x2="{1}" y1="{2}" y2="{2}" />\n'.format(width*0.09,width*0.11,height*0.3)
	svg += '<line stroke="rgb(10%,10%,16%)" x1="{0}" x2="{1}" y1="{2}" y2="{2}" />\n'.format(width*0.09,width*0.11,height*0.1)
	svg += '</g>'
	
	return svg

def y_axis_name(maxValue,numberOfValues,height,width):
	cursor = 0

	svg = '<g id="yAxisLegend">'
	svg += '<text x="{}" y="{}">{:.0f}</text> \n'.format(width*0.05,height*0.705,maxValue*0.25)
	svg += '<text x="{}" y="{}">{:.0f}</text> \n'.format(width*0.05,height*0.505,maxValue*0.5)
	svg += '<text x="{}" y="{}">{:.0f}</text> \n'.format(width*0.05,height*0.305,maxValue*0.75)
	svg += '<text x="{}" y="{}">{:.0f}</text> \n'.format(width*0.05,height*0.105,maxValue)
	svg += '</g>'

	return svg

def x_axis_bars(answers,height,width): #TODO: Bars und Beschriftung auseinanderfummeln
	barProcent = width*(0.7 / len(answers))
	scale = (1/max_number(answers)) * (height * 0.8)
	cursor = width*0.12
	svg = '<g id="bars">'
	#textLength="{2}"
	for answer in answers:
		barheight = answer["number"] * scale
		svg += '<text x="{0}" y="{1}" textLength="50" lengthAdjust="spacing" >{3}</text> \n'.format(cursor,height*0.95,height*0.1,answer["text"])
		svg +='<rect x="{0}" y="{1}" width="{2}" height="{3}" style="fill:rgb(0,0,139);" />\n'.format(cursor,(height*0.9)-barheight,barProcent*0.8,barheight)
		cursor += barProcent

	svg += "</g>"
	return svg

	

def create_bardiagram(question,height,width):
	svg ='<svg baseProfile="tiny" height="100%" version="1.2" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs />\n'
	svg += create_blank_bardiagram(height,width)
	svg += y_axis_name(max_number(question["answers"]),4,height,width)
	svg += x_axis_bars(question["answers"],height,width)
	svg += '</svg>'
	return svg
	


def create_report_svg(reportJSON,outputfile):

	with open(reportJSON) as f:

		report = json.load(f)
		i = 0
		html = '<html><head><title>A report</title></head><body>\n <ul> \n'

		for question in report:

			html += '<li>\n'
			html += '<h1>{}</h1>\n'.format(question["question"])
			html += create_bardiagram(question,700,700)
			html += '</li>\n'

		html += '<ul>\n</body>\n</html>'
		with open(outputfile,'w') as f:
			f.write(html)

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="Takes a report.json and builds a .svg")
	parser.add_argument("-i","--input", nargs=1, help="The report.json inputfile", required=True)
	parser.add_argument("-o","--output", nargs=1, help="The output .html file", required=True)

	args = parser.parse_args()


	create_report_svg(args.input[0],args.output[0])