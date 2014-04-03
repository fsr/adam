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
	refPoint = ctx.get_current_point()

	ctx.rel_move_to(0.1*width,0.1*height)   #TODO: Fancy arrowheads for the axis ends
	ctx.rel_line_to(0,0.8*height)
	ctx.rel_move_to(-0.1*width,-0.1*height)
	ctx.rel_line_to(width,0)

	ctx.move_to(*refPoint)
	

def textBox(ctx,height,width):
	#TODO: Scales a text to a given box
	return 0


def y_axis_label(ctx,maxValue,numberOfValues,height,width):
	refPoint = ctx.get_current_point()

	diffMarker = (0.9*(0.7*height)) / numberOfValues 
	diffValue = maxValue / numberOfValues
	value = diffValue
	ctx.rel_move_to(0.125*width,0.8*height)

	for _ in range(numberOfValues):
			ctx.rel_move_to(-0.05*width,-diffMarker)
			ctx.rel_line_to(0.05*width,0)

			textPoint = ctx.get_current_point()
			ctx.rel_move_to(-0.10*width,0.007*height)
			ctx.show_text('{}'.format(int(value)))
			value += diffValue
			ctx.move_to(*textPoint)

	ctx.move_to(*refPoint)



def x_axis_label(ctx,answers,height,width): 
	#TODO: Implementation
	return 0

def create_bars(ctx,answers,height,width):
	refPoint = ctx.get_current_point()

	barWidth = width*(0.7 / len(answers))
	scaleFactor =  (0.9*(0.7*height)) /max_number(answers)
	xCursor = refPoint[0] + (0.15*width)

	for answer in answers:

		barHeight = answer["number"] * scaleFactor
		yCursor =  refPoint[1]+((0.8*height)-barHeight)
		ctx.rectangle(xCursor,yCursor,barWidth*0.8,barHeight)
		xCursor += barWidth

	ctx.move_to(*refPoint)



def create_bardiagram(ctx,question,height,width):
	
	curX = ctx.get_current_point()[0]
	curY = ctx.get_current_point()[1]

	ctx.rectangle(curX,curY,height,width)
	create_blank_bardiagram(ctx,height,width)
	y_axis_label(ctx,max_number(question["answers"]),5,height,width)
	create_bars(ctx,question["answers"],height,width)

	ctx.stroke()

	


def create_report_pdf(reportJSON,outputfile):
	mySurface = cairo.PDFSurface(outputfile,595,842)
	ctx = cairo.Context(mySurface)
	ctx.move_to(0,0)

	

	with open(reportJSON) as f:

		report = json.load(f)
		curX = 0
		curY = 0

		for question in report:

			create_bardiagram(ctx,question, 595/2,842/3)


			#TODO: Put this in a function, add multiple page support
			curX  += 595/2
			if curX >= 595:
				curX = 0
				curY += 842/3

			if curY >= 842:
				print("New Page!")


			ctx.move_to(curX,curY)
		
	


	
		

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="Takes a report.json and builds a .pdf")
	parser.add_argument("-i","--input", nargs=1, help="The report.json inputfile", required=True)
	parser.add_argument("-o","--output", nargs=1, help="The output .pdf file", required=True)

	args = parser.parse_args()

	create_report_pdf(args.input[0],args.output[0])


