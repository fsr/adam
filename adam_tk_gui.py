#!/usr/bin/env python3

import os
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
		tk.Button(self, text = "...", command = self.openquestions).grid(row=0, column=1)
		self.questionsfilename_label = tk.Label(self, text="", font="TkFixedFont")
		self.questionsfilename_label.grid(row=0, column=2, sticky="W")
		
		tk.Label(self, text="Answers list (JSON):").grid(row=1, column=0, sticky="E")
		tk.Button(self, text = "...", command = self.openanswers).grid(row=1, column=1)
		self.answersfilename_label = tk.Label(self, text="", font="TkFixedFont")
		self.answersfilename_label.grid(row=1, column=2, sticky="W")
		
		#tk.Frame(height=2, bd=1, relief="sunken").pack(fill="x", padx=5, pady=5)
		#.grid(row=2, column=0)#columnspan=3, sticky="W", padx=5, pady=5)
		
		tk.Label(self, text="Result database (sqlite db):").grid(row=3, column=0, sticky="E")
		tk.Button(self, text = "...", command = self.opendb).grid(row=3, column=1)
		self.dbfilename_label = tk.Label(self, text="", font="TkFixedFont")
		self.dbfilename_label.grid(row=3, column=2, sticky="W")
		
		# TODO separator of some sort at row 4?
		
		tk.Label(self, text="Report definition (JSON):").grid(row=5, column=0, sticky="E")
		tk.Button(self, text = "...", command = self.openreportdef).grid(row=5, column=1)
		self.reportdeffilename_label = tk.Label(self, text="", font="TkFixedFont")
		self.reportdeffilename_label.grid(row=5, column=2, sticky="W")
		
		#self.grid_columnconfigure(2, {"minsize": 200})
	
	def openquestions(self):
		filename = askopenfilename()
		if not filename == "":
			questionsfilename = filename
			self.questionsfilename_label["text"] = os.path.basename(filename)
	
	def openanswers(self):
		filename = askopenfilename()
		if not filename == "":
			answersfilename = filename
			self.answersfilename_label["text"] = os.path.basename(filename)
	
	def opendb(self):
		filename = askopenfilename()
		if not filename == "":
			dbfilename = filename
			self.dbfilename_label["text"] = os.path.basename(filename)
			# TODO read table list and populate combobox with courses
	
	def openreportdef(self):
		filename = askopenfilename()
		if not filename == "":
			reportdeffilename = filename
			self.reportdeffilename_label["text"] = os.path.basename(filename)

root = tk.Tk()
app = App(master=root)
app.mainloop()
