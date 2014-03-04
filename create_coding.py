#!/usr/bin/python3
from gi.repository import Gtk, Gio
import json

def parse_course_data_from_file(filename):
	# Tail-recursionesque ideas for the win.
	courses = []
	with open(filename, "r") as course_file:
		for line in course_file:
			# Remove newline at the end
			line = line[:-1]
			# Filter comments
			if line.startswith("#") or not line:
				continue
				
			# New course has started, start new course block
			if not line.startswith("\t"):
				course_name = (line[::-1].split("(", 1))[1][::-1].strip()
				course_lect = (line[::-1].split("(", 1))[0][:0:-1].strip()
				courses.append({"name": course_name, "lecturer": course_lect, "tutors": []})
				continue
				
			# So we have at least one indentation level, trim it:
			line = line[1:]
			# New tutor starts
			if not line.startswith("\t"):
				reversed_name_array = line[::-1].split(" ", 1)
				if len(reversed_name_array) == 1:
					first = ""
					last = line
				else:
					first = reversed_name_array[1][::-1].strip()
					last  = reversed_name_array[0][::-1].strip()
				courses[-1]["tutors"].append({"firstname": first, "lastname": last, "exercises": []})
				continue
			
			# Two tabs or more means we have to parse exercises
			exercise = line.strip().split(",",-1)
			if len(exercise) != 3: raise Exception("Line '" + line + "'is not a valid exercise")
			
			if   exercise[0] in ["Monday",    "Montag",     "Mo", "Mo"]: weekday = 0
			elif exercise[0] in ["Tuesday",   "Dienstag",   "Tu", "Di"]: weekday = 1
			elif exercise[0] in ["Wednesday", "Mittwoch",   "We", "Mi"]: weekday = 2
			elif exercise[0] in ["Thursday",  "Donnerstag", "Th", "Do"]: weekday = 3
			elif exercise[0] in ["Friday",    "Freitag",    "Fr", "Fr"]: weekday = 4
			else: raise Exception("Weekday '" + exercise[0] + "' is not valid")
			
			courses[-1]["tutors"][-1]["exercises"].append(
				{"day": weekday, "time": int(exercise[1].strip()[:1]), "place": exercise[2].strip()});
		
	# Gonna use this soon.		
	def exercise_timevalue(e):
		return e["day"]*24 + e["time"] # 24 is rather arbitrary
				
	for course in courses:
		# With everything read, sort everything starting with individual exercises per tutor...
		for tutor in course["tutors"]:
			tutor["exercises"].sort(key=exercise_timevalue)
		# ...to continue sorting the tutors accordingly
		course["tutors"].sort(key=lambda t: exercise_timevalue(t["exercises"][0]))
		# Then generate codes for tutors
		code = 1
		for tutor in course["tutors"]:
			tutor["code"] = code
			code += 1
			
	return courses

class GenerateCodingWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="Generate coding")
		
		# HeaderBar
		
		self.hb = Gtk.HeaderBar()
		self.hb.props.show_close_button = True
		self.hb.props.title = "HeaderBar example"
		self.set_titlebar(self.hb)
		
		self.choose_file_button = Gtk.Button()
		icon = Gio.ThemedIcon(name="document-open")
		image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
		self.choose_file_button.add(image)
		self.choose_file_button.connect("clicked", self.choose_file_click)
		self.hb.pack_start(self.choose_file_button)
		
		# Lower Grid
		
		self.table = Gtk.Grid()
		self.table.set_column_homogeneous(True)
		self.add(self.table)
		
		self.file_list = Gtk.TreeView()
		self.file_list.set_vexpand(True)
		self.table.attach(self.file_list, 0, 0, 1, 1)
		
		self.scrolledwindow = Gtk.ScrolledWindow()
		self.scrolledwindow.set_hexpand(True)
		self.scrolledwindow.set_vexpand(True)
		self.json_text = Gtk.TextView()
		self.json_text.set_vexpand(True)
		self.scrolledwindow.add(self.json_text)
		self.table.attach(self.scrolledwindow, 1, 0, 1, 1)
		
		self.file_choice_box = Gtk.Box(spacing=6)
		self.table.attach(self.file_choice_box, 0, 1, 2, 1)
		
		self.filename_entry = Gtk.Entry(text="example_files/course_abc.txt")
		self.file_choice_box.pack_start(self.filename_entry, True, True, 0)
		
		self.load_courses_button = Gtk.Button(label="Load")
		self.load_courses_button.connect("clicked", self.load_courses)
		self.file_choice_box.pack_start(self.load_courses_button, True, True, 0)
		
		self.generate_coding_button = Gtk.Button(label="Generate coding")
		self.generate_coding_button.connect("clicked", self.print_coding)
		self.file_choice_box.pack_start(self.generate_coding_button, True, True, 0)
		

	def choose_file_click(self, widget):
		dialog = Gtk.FileChooserDialog("Choose course file", self,
			Gtk.FileChooserAction.OPEN,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			 Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			self.filename_entry.set_text(dialog.get_filename())

		dialog.destroy()
		
	def load_courses(self, widget):
		parse_course_data_from_file(self.filename_entry.get_text())

	def print_coding(self, widget):
		pprint.pprint(courses)

def show_coding_window():
	win = GenerateCodingWindow()
	win.connect("delete-event", Gtk.main_quit)
	win.show_all()
	Gtk.main()

show_coding_window()
courses = parse_course_data_from_file("example_files/course_abc.txt")
courses.extend(parse_course_data_from_file("example_files/course_xyz.txt"))
print(json.dumps(courses, indent=4, sort_keys=True))
