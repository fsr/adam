#!/usr/bin/python

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
	ctx.save()

	ctx.rel_move_to(0.1*width,0.1*height)   #TODO: Fancy arrowheads for the axis ends
	ctx.rel_line_to(0,0.8*height)
	ctx.rel_move_to(-0.1*width,-0.1*height)
	ctx.rel_line_to(width,0)
	
	ctx.restore()

def y_axis_label(ctx,maxValue,numberOfValues,height,width):
	ctx.save()

	distanceMarker = (0.9*(0.7*height)) / numberOfValues 
	differenceValue = maxValue / numberOfValues
	value = differenceValue
	ctx.rel_move_to(0.125*width,0.8*height)

	for _ in range(numberOfValues):
			ctx.save()

			ctx.rel_move_to(-0.05*width,-distanceMarker)
			ctx.rel_line_to(0.05*width,0)

			ctx.restore()

	ctx.restore()

def x_axis_label(answers,height,width): 
	#TODO: Implementation
	return 0

def create_bars(answers,height,width):
	#TODO: Implementation
	return 0

def create_bardiagram(ctx,question,height,width):
	
	ctx.rectangle(0,0,200,200)

	ctx.move_to(0,0)
	create_blank_bardiagram(ctx,200,200)
	ctx.stroke()
	ctx.move_to(0,0)
	y_axis_label(ctx,200,4,200,200)
	ctx.stroke()

	


def create_report_pdf(reportJSON,outputfile):
	mySurface = cairo.PDFSurface(outputfile,595,842)
	myContext = cairo.Context(mySurface)

	create_bardiagram(myContext,"Test", 100,100)
	
	


	
		

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="Takes a report.json and builds a .pdf")
	parser.add_argument("-i","--input", nargs=1, help="The report.json inputfile", required=True)
	parser.add_argument("-o","--output", nargs=1, help="The output .pdf file", required=True)

	args = parser.parse_args()

	



	create_report_pdf(args.input[0],args.output[0])


