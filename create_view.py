# !/usr/bin/python

import json
import argparse
import cairo
from math import pi
# light blue      light green     light violet	   light brown  light yellow    blue             green 			    grey
color = [(0.706, 1, 0.412), (0.412, 0.706, 1), (0.706, 0.412, 1), (1, 0.706, 0.412), (1, 1, 0.412), (0.412, 0.412, 1),
         (0.412, 1, 0.412), (0.412, 0.412, 0.412)]

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
def text_box(ctx, text, width, height):
    refPoint = ctx.get_current_point()
    ctx.save()

    extents = ctx.text_extents(text)
    fontSize = ctx.font_extents()[0]

    while extents[2] > width or extents[3] > height:
        ctx.set_font_size(fontSize)
        extents = ctx.text_extents(text)
        fontSize -= 1

    midX = (refPoint[0] + (width / 2)) - ((extents[2] / 2) + extents[0])
    midY = (refPoint[1] + (height / 2)) - ((extents[3] / 2) + extents[1])
    ctx.move_to(midX, midY)
    ctx.show_text(text)
    #for positioning
    #ctx.rectangle(refPoint[0],refPoint[1],width,height)
    #ctx.rel_move_to(width*0.5,0)
    #ctx.rel_line_to(0,-height*0.8)

    ctx.restore()
    ctx.move_to(*refPoint)


#creates the axis for a bardiagram
#parameter: ctx = context obj, height = abs. height of the bardiagram, width = abs. width of the bardiagram
#the reference point is the top left corner of bardiagram, the current point is not altered
def create_blank_bardiagram(ctx, width, height):
    refPoint = ctx.get_current_point()

    ctx.rel_move_to(0.1 * width, 0.1 * height)  #TODO: Fancy arrowheads for the axis ends
    ctx.rel_line_to(0, 0.8 * height)
    ctx.rel_move_to(-0.1 * width, -0.1 * height)
    ctx.rel_line_to(width * 0.9, 0)

    ctx.move_to(*refPoint)


#creates the labels of the y-axis
#parameter: ctx = context obj., maxValue = the maximum value for the highest label, numberOfLabels = the number of labels that should be created, height = abs. height of the bardiagram, width = abs. width of the bardiagram
#the reference point is the top left corner of bardiagram
def y_axis_label(ctx, maxValue, numberOfLabels, width, height):
    refPoint = ctx.get_current_point()

    diffMarker = (0.9 * (0.7 * height)) / numberOfLabels
    diffValue = maxValue / numberOfLabels
    value = diffValue
    ctx.rel_move_to(0.125 * width, 0.8 * height)

    for _ in range(numberOfLabels):
        ctx.rel_move_to(-0.05 * width, -diffMarker)
        ctx.rel_line_to(0.05 * width, 0)

        textPoint = ctx.get_current_point()
        ctx.rel_move_to(-0.11 * width, -0.0235 * height)
        text_box(ctx, str(int(value)), 0.05 * width, 0.05 * height)
        value += diffValue
        ctx.move_to(*textPoint)

    ctx.move_to(*refPoint)


def x_axis_label(ctx, answers, width, height):
    refPoint = ctx.get_current_point()
    ctx.save()

    barWidth = width * (0.7 / len(answers))

    #positioning of the coordinatesystem
    ctx.translate(refPoint[0] + (0.15 * width), refPoint[1] + (0.99 * height))
    ctx.rotate(-pi * 0.5)
    ctx.move_to(0, 0)

    for answer in answers:
        #string cutting for strings >20 chars
        #text = (answer["text"][:20] + '..') if len(answer["text"]) > 20 else answer["text"]
        text = answer["text"]
        text_box(ctx, text, 0.18 * height, barWidth * 0.8)
        ctx.rel_move_to(0, barWidth)

    ctx.restore()
    ctx.move_to(*refPoint)


def x_axis_label_layers(ctx, answers, width, height):
    refPoint = ctx.get_current_point()
    ctx.save()

    barWidth = width * (0.7 / len(answers))

    moveDown = True
    ctx.rel_move_to((width * 0.15) - (barWidth * 0.4), (height * 0.8))

    for answer in answers:
        text_box(ctx, answer["text"], barWidth * 1.6, height * 0.1)

        if moveDown == True:
            ctx.rel_move_to(barWidth, height * 0.05)
            moveDown = False

        else:
            ctx.set_line_width(0.01)
            ctx.rel_move_to(barWidth * 0.8, 0)
            ctx.rel_line_to(0, -(height * 0.05))
            ctx.rel_move_to(0, (height * 0.05))
            ctx.rel_move_to(barWidth * 0.2, -(height * 0.05))
            moveDown = True

    ctx.restore()
    ctx.move_to(*refPoint)


#adds the path for all bars
#parameter: ctx = context obj, answers = list with answers, 
def create_bars(ctx, answers, width, height):
    refPoint = ctx.get_current_point()

    barWidth = width * (0.7 / len(answers))
    scaleFactor = (0.9 * (0.7 * height)) / max_number(answers)
    xCursor = refPoint[0] + (0.15 * width)

    for answer in answers:
        barHeight = answer["number"] * scaleFactor
        yCursor = refPoint[1] + ((0.8 * height) - barHeight)
        ctx.rectangle(xCursor, yCursor, barWidth * 0.8, barHeight)
        xCursor += barWidth

    ctx.move_to(*refPoint)


#creates a simpel bardiagram
#parameter: ctx = context Obj, question = one question object, width = abs. width of the bardiagram, height = abs. height of the bardiagram
def create_bardiagram(ctx, question, width, height):
    refPoint = ctx.get_current_point()
    ctx.save()
    #Only for help TODO: Remove this block
    curX = ctx.get_current_point()[0]
    curY = ctx.get_current_point()[1]
    ctx.rectangle(curX, curY, width, height)

    #diagram
    create_blank_bardiagram(ctx, width, height)
    y_axis_label(ctx, max_number(question["answers"]), 4, width, height)


    #text
    ctx.save()
    ctx.set_font_size(8)
    x_axis_label(ctx, question["answers"], width, height)
    ctx.restore()
    ctx.rel_move_to(0.1 * width, 0)
    text_box(ctx, question["question"], 0.8 * width, 0.1 * height)

    ctx.stroke()

    #bars
    ctx.set_source_rgb(0.15, 0.5, 1.0)
    ctx.move_to(*refPoint)
    create_bars(ctx, question["answers"], width, height)

    ctx.fill()

    ctx.restore()
    ctx.move_to(*refPoint)


def create_cakediagram(ctx, question, width, height):
    refPoint = ctx.get_current_point()
    ctx.save()

    #TODO: Remove this block
    curX = ctx.get_current_point()[0]
    curY = ctx.get_current_point()[1]
    ctx.rectangle(curX, curY, width, height)

    radius = width if width < height else height
    radius *= 0.45

    ctx.rel_move_to((width / 2), (height / 2))
    centerPoint = ctx.get_current_point()
    ctx.stroke()
    ctx.move_to(*centerPoint)
    scaleFactor = (2 * pi) / sum_numbers(question["answers"])
    arcStart = 0
    i = 0

    for answer in question["answers"]:
        ctx.save()

        arcEnd = arcStart + (answer["number"] * scaleFactor)
        ctx.arc(centerPoint[0], centerPoint[1], radius, arcStart, arcEnd)
        ctx.line_to(*centerPoint)
        arcStart = arcEnd

        ctx.set_source_rgb(*color[i])
        ctx.fill()

        i += 1
        if i >= len(color):
            i = 0

        ctx.restore()

    ctx.restore()
    ctx.move_to(*refPoint)


def create_report_pdf(reportJSON, outputfile):
    mySurface = cairo.PDFSurface(outputfile, 595, 842)
    ctx = cairo.Context(mySurface)
    ctx.move_to(0, 0)

    with open(reportJSON) as f:

        report = json.load(f)
        curX = 0
        curY = 0

        for question in report:

            if (question["view"] == "bardiagram"):
                create_bardiagram(ctx, question, 595 / 2, 842 / 3)
            if (question["view"] == "cakediagram"):
                create_cakediagram(ctx, question, 595 / 2, 842 / 3)

            #TODO: Put this in a function
            curX += 595 / 2
            if curX >= 595:
                curX = 0
                curY += 842 / 3

            if curY >= 842:
                ctx.show_page()  # creates a new page
                curX = 0
                curY = 0

            ctx.move_to(curX, curY)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Takes a report.json and builds a .pdf")
    parser.add_argument("-i", "--input", nargs=1, help="The report.json inputfile", required=True)
    parser.add_argument("-o", "--output", nargs=1, help="The output .pdf file", required=True)

    args = parser.parse_args()

    create_report_pdf(args.input[0], args.output[0])


