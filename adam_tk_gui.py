#!/usr/bin/env python3

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import font

# The master GUI suite programm thing.

questionsfilename = ""
answersfilename = ""
dbfilename = ""
reportdeffilename = ""

class App(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.pack()
		
		tk.Label(self, text="Question list (JSON):").grid(row=0, column=0, sticky="E")
		self.questionsfilename_label = tk.Label(self, text="", font="TkFixedFont")
		self.questionsfilename_label.grid(row=0, column=1, sticky="W")
		tk.Button(self, text = "...", command = self.openquestions).grid(row=0, column=2)
		
		tk.Label(self, text="Answers list (JSON):").grid(row=1, column=0, sticky="E")
		self.answersfilename_label = tk.Label(self, text="", font="TkFixedFont")
		self.answersfilename_label.grid(row=1, column=1, sticky="W")
		tk.Button(self, text = "...", command = self.openanswers).grid(row=1, column=2)
		
		tk.Label(self, text="Result database (sqlite db):").grid(row=2, column=0, sticky="E")
		self.dbfilename_label = tk.Label(self, text="", font="TkFixedFont")
		self.dbfilename_label.grid(row=2, column=1, sticky="W")
		tk.Button(self, text = "...", command = self.opendb).grid(row=2, column=2)
		
		# TODO separator of some sort at row 3?
		
		tk.Label(self, text="Report definition (JSON):").grid(row=4, column=0, sticky="E")
		self.reportdeffilename_label = tk.Label(self, text="", font="TkFixedFont")
		self.reportdeffilename_label.grid(row=4, column=1, sticky="W")
		tk.Button(self, text = "...", command = self.openreportdef).grid(row=4, column=2)
		
	
	def openquestions(self):
		filename = askopenfilename()
		if not filename == "":
			questionsfilename = filename
			self.questionsfilename_label["text"] = filename
	
	def openanswers(self):
		filename = askopenfilename()
		if not filename == "":
			answersfilename = filename
			self.answersfilename_label["text"] = filename
	
	def opendb(self):
		filename = askopenfilename()
		if not filename == "":
			dbfilename = filename
			self.dbfilename_label["text"] = filename
			# TODO read table list and populate combobox with courses
	
	def openreportdef(self):
		filename = askopenfilename()
		if not filename == "":
			reportdeffilename = filename
			self.reportdeffilename_label["text"] = filename

root = tk.Tk()
app = App(master=root)
app.mainloop()
