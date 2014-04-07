#!/usr/bin/env python3

import os
import json
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import font

import get_result
import create_coding
import construct_report
import create_view

# The master GUI suite programm thing.

class App(tk.Frame):
	questionsfilename = ""
	answersfilename = ""
	dbfilename = ""
	reportdeffilename = ""

	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.pack()
		
		#self.grid_columnconfigure(2, {"minsize": 200})
		
		tk.Label(self, text="Question list (JSON):").grid(row=0, column=0, sticky="E")
		tk.Button(self, text = "...", command = self.openquestions).grid(row=0, column=1)
		self.questionsfilename_label = tk.Label(self, text="", font="TkFixedFont")
		self.questionsfilename_label.grid(row=0, column=2, sticky="W")
		
		tk.Label(self, text="Answers list (JSON):").grid(row=1, column=0, sticky="E")
		tk.Button(self, text = "...", command = self.openanswers).grid(row=1, column=1)
		self.answersfilename_label = tk.Label(self, text="", font="TkFixedFont")
		self.answersfilename_label.grid(row=1, column=2, sticky="W")
		
		tk.Frame(self, height=2, bd=1, relief="sunken").grid(row=2, column=0, columnspan=3, sticky="EW", padx=5, pady=5)
		
		tk.Label(self, text="Result database (sqlite db):").grid(row=3, column=0, sticky="E")
		tk.Button(self, text = "...", command = self.opendb).grid(row=3, column=1)
		self.dbfilename_label = tk.Label(self, text="", font="TkFixedFont")
		self.dbfilename_label.grid(row=3, column=2, sticky="W")
		
		tk.Label(self, text="Course (from DB):").grid(row=4, column=0, sticky="E")
		self.coursevar = tk.StringVar(master)
		self.table_box = tk.OptionMenu(self, self.coursevar, "foo")
		self.table_box.grid(row=4, column=2, sticky="W")
		
		tk.Frame(self, height=2, bd=1, relief="sunken").grid(row=5, column=0, columnspan=3, sticky="EW", padx=5, pady=5)
		
		tk.Label(self, text="Report definition (JSON):").grid(row=6, column=0, sticky="E")
		tk.Button(self, text = "...", command = self.openreportdef).grid(row=6, column=1)
		self.reportdeffilename_label = tk.Label(self, text="", font="TkFixedFont")
		self.reportdeffilename_label.grid(row=6, column=2, sticky="W")
		
		tk.Frame(self, height=2, bd=1, relief="sunken").grid(row=7, column=0, columnspan=3, sticky="EW", padx=5, pady=5)
		tk.Frame(self, height=2, bd=1, relief="sunken").grid(row=8, column=0, columnspan=3, sticky="EW", padx=5, pady=5)
		
		tk.Button(self, text = "Create PDF", command = self.create_pdf).grid(row=9, column=0, columnspan=3)
	
	def openquestions(self):
		filename = askopenfilename()
		if not filename == "":
			self.questionsfilename = filename
			self.questionsfilename_label["text"] = os.path.basename(filename)
	
	def openanswers(self):
		filename = askopenfilename()
		if not filename == "":
			self.answersfilename = filename
			self.answersfilename_label["text"] = os.path.basename(filename)
	
	def opendb(self):
		filename = askopenfilename()
		if not filename == "":
			self.dbfilename = filename
			self.dbfilename_label["text"] = os.path.basename(filename)
			
			self.coursevar.set("")
			self.table_box["menu"].delete(0, "end")
			
			tables = get_result.get_courses(filename)
			
			for choice in tables:
				self.table_box['menu'].add_command(label=choice, command=tk._setit(self.coursevar, choice))
	
	def openreportdef(self):
		filename = askopenfilename()
		if not filename == "":
			self.reportdeffilename = filename
			self.reportdeffilename_label["text"] = os.path.basename(filename)
	
	def create_pdf(self):
		filename = asksaveasfilename(title="Save as PDF (additional .json file will be created)", filetypes=[("PDF", "*.pdf")])
		if not filename == "":
			# Create report first...
			with open(self.reportdeffilename, 'r') as f:
				reportdef = json.load(f)
			with open(self.questionsfilename, 'r') as f:
				questionsdef = json.load(f)
			with open(self.answersfilename, 'r') as f:
				answersdef = json.load(f)
			
			report = construct_report.construct_report(reportdef, questionsdef, answersdef, self.dbfilename, self.coursevar.get())
			report_json = create_coding.prettyprint_json(report)
			
			jsonfilename = "{}.json".format(filename)
			with open(jsonfilename, 'w') as f:
				f.write(report_json)
				
			# ...then render it.
			create_view.create_report_pdf(jsonfilename, filename)

root = tk.Tk()
app = App(master=root)
app.mainloop()
