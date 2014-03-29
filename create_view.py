#!usr/bin/python

import json
import argparse
import cairo

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

#parameter: ctx = context Obj, height = abs. height of the dia, width = abs. width of the dia
def create_blank_bardiagram(ctx,height,width):
	ctx.rel_move_to(0.1*width,0.1*height)   #TODO: Fancy arrowheads for the axis ends
	ctx.rel_line_to(0,0.8*height)
	ctx.rel_move_to(-0.1*width,-0.1*height)
	ctx.rel_line_to(width,0)
	ctx.stroke()#TODO: Replace with a move_to old position


def y_axis_label(ctx,maxValue,numberOfValues,height,width):
	distanceMarker = (0.9*(0.7*height)) / numberOfValues
	ctx.rel_move_to(0.125*width,0.8*height) 
	differenceValue = maxValue / numberOfValues
	value = differenceValue

	for _ in range(numberOfValues):
			ctx.rel_move_to(-0.05*width,-distanceMarker)
			ctx.rel_line_to(0.05*width,0)
			ctx.rel_move_to(-0.125*width,0.25*distanceMarker)
			ctx.show_text('{}'.format(int(value)))
			ctx.rel_move_to(,-0.25*distanceMarker)
			value += differenceValue

	ctx.stroke() #TODO: Replace with a move_to old position

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

	parser = argparse.ArgumentParser(description="Takes a report.json and builds a .pdf")
	parser.add_argument("-i","--input", nargs=1, help="The report.json inputfile", required=True)
	parser.add_argument("-o","--output", nargs=1, help="The output .pdf file", required=True)

	args = parser.parse_args()

	mySurface = cairo.PDFSurface("Test.pdf",595,842)
	myContext = cairo.Context(mySurface)
	
	myContext.rectangle(0,0,200,200)

	myContext.move_to(0,0)
	create_blank_bardiagram(myContext,200,200)
	myContext.move_to(0,0)
	y_axis_label(myContext,200,4,200,200)


	create_report_pdf(args.input[0],args.output[0])


