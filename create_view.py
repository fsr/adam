#!/usr/bin/python

import json
import argparse
import cairo
from math import pi

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

#scales a text down that is to big to fit the specified box 
#parameter: ctx = context obj, height = abs. height of the box, width = abs. width of the box
#the reference point is the top left corner, the current point is not altered
def text_box(ctx,text,width,height):
	refPoint = ctx.get_current_point()
	refFontSize = ctx.font_extents()[0]

	extents = ctx.text_extents(text)
	fontSize = refFontSize

	while extents[2] > width or extents[3] > height:
		ctx.set_font_size(fontSize)
		extents = ctx.text_extents(text)
		fontSize -= 1

	midX = (refPoint[0] + (width/2)) - ((extents[2]/2) + extents[0])
	midY = (refPoint[1] + (height/2)) - ((extents[3]/2) + extents[1])
	ctx.move_to(midX,midY)
	ctx.show_text(text)
	#for positioning
	#ctx.rectangle(refPoint[0],refPoint[1],width,height)

	
	ctx.set_font_size(refFontSize)
	ctx.move_to(*refPoint)
#creates the axis for a bardiagram
#parameter: ctx = context obj, height = abs. height of the bardiagram, width = abs. width of the bardiagram
#the reference point is the top left corner of bardiagram, the current point is not altered
def create_blank_bardiagram(ctx,width,height):
	refPoint = ctx.get_current_point()

	ctx.rel_move_to(0.1*width,0.1*height)   #TODO: Fancy arrowheads for the axis ends
	ctx.rel_line_to(0,0.8*height)
	ctx.rel_move_to(-0.1*width,-0.1*height)
	ctx.rel_line_to(width,0)

	ctx.move_to(*refPoint)


#creates the labels of the y-axis
#parameter: ctx = context obj., maxValue = the maximum value for the highest label, numberOfLabels = the number of labels that should be created, height = abs. height of the bardiagram, width = abs. width of the bardiagram
#the reference point is the top left corner of bardiagram
def y_axis_label(ctx,maxValue,numberOfLabels,width,height):
	refPoint = ctx.get_current_point()

	diffMarker = (0.9*(0.7*height)) / numberOfLabels 
	diffValue = maxValue / numberOfLabels
	value = diffValue
	ctx.rel_move_to(0.125*width,0.8*height)

	for _ in range(numberOfLabels):
			ctx.rel_move_to(-0.05*width,-diffMarker)
			ctx.rel_line_to(0.05*width,0)

			textPoint = ctx.get_current_point()
			ctx.rel_move_to(-0.11*width,-0.0235*height)
			text_box(ctx,str(int(value)),0.05*width,0.05*height)
			value += diffValue
			ctx.move_to(*textPoint)

	ctx.move_to(*refPoint)

def x_axis_label(ctx,answers,width,height): 
	refPoint = ctx.get_current_point()

	yCursor = refPoint[0] + (0.15*width)
	barWidth = width*(0.7 / len(answers))

	ctx.rotate(-0.5*pi)

	ctx.rel_move_to(0,yCursor)
	ctx.rel_line_to(100,0)
	


	ctx.rotate(0.5*pi)

	ctx.move_to(*refPoint)

#adds the path for all bars
#parameter: ctx = context obj, answers = list with answers, height = abs. height of the bardiagram, width = abs. width of the bardiagram
def create_bars(ctx,answers,width,height):
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


#creates a simpel bardiagram
def create_bardiagram(ctx,question,width,height):
	
	#Only for help
	curX = ctx.get_current_point()[0]
	curY = ctx.get_current_point()[1]
	ctx.rectangle(curX,curY,width,height)

	#diagram
	create_blank_bardiagram(ctx,width,height)
	y_axis_label(ctx,max_number(question["answers"]),4,width,height)
	

	#text	
	#x_axis_label(ctx,question["question"],width,height)
	ctx.rel_move_to(0.1*width,0)
	text_box(ctx,question["question"],0.8*width,0.1*height)
	ctx.stroke()

	#bars
	ctx.set_source_rgb(0.15,0.5,1.0)
	ctx.move_to(curX,curY)
	create_bars(ctx,question["answers"],width,height)
	ctx.fill()
	ctx.set_source_rgb(0.0,0.0,0.0)

	
def create_report_pdf(reportJSON,outputfile):
	mySurface = cairo.PDFSurface(outputfile,595,842)
	ctx = cairo.Context(mySurface)
	ctx.move_to(0,0)

	with open(reportJSON) as f:

		report = json.load(f)
		curX = 0
		curY = 0

		for question in report:

			create_bardiagram(ctx,question,595/2,842/3)


			#TODO: Put this in a function
			curX  += 595/2
			if curX >= 595:
				curX = 0
				curY += 842/3

			if curY >= 842:
				ctx.show_page()
				curX = 0
				curY = 0


			ctx.move_to(curX,curY)
		
if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="Takes a report.json and builds a .pdf")
	parser.add_argument("-i","--input", nargs=1, help="The report.json inputfile", required=True)
	parser.add_argument("-o","--output", nargs=1, help="The output .pdf file", required=True)

	args = parser.parse_args()

	create_report_pdf(args.input[0],args.output[0])


