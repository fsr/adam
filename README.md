Adam
====

Adam is a tool usable for the teaching evaluation at the TU Dresden.
This version is completely rewritten using Python3 based on the most simple and basic requirements.
A basic GUI written for GTK3 is available for parts of the functionality.

Usage
-----

### Create tutor coding ###

#### JSON coding creation ####

`create_coding.py` can load multiple plain text files containing data about courses and their tutors and produce the corresponding JSON coding.
This JSON data can be printed to stdout:

	# Create coding from one or multiple plain text files
	create_coding.py course_abc.txt course_xyz.txt

Alternatively you can specify a file to save to save the coding to:

	create_coding.py course_abc.txt course_xyz.txt -o file.json

This stdout/output-choice also exists in other modules.

If you want to / can use the GUI, simply call `coding_gui.py`:

	coding_gui.py

#### Export into readable formats ####

`export_coding.py` takes the created JSON files and produces readable files from it:
either a simple plain text file

	export_coding.py plain -o outfile coding.json

or a fancy html table (that can be used for printing and showing in the lectures)

	export_coding.py html -o outfile.htm -s example_files/slides.css coding.json

### Prepare question data ###

`json_questions.py` can load a plain text question form definition and convert it into a processable JSON file.
Additionally these JSON files an be validated against a answer type definition file.

	json_questions.py -o eva_questions_pre_SS14.json -d example_files/eva_answertypes.json example_files/eva_questions_pre_SS14

### Import CSV into sqlite database ###

`create_table.py` takes .csv files and inserts them into a sqlite database, use it like this:

	# importing a directory:
	create_table.py -d TestDB.db dir someDirectory

	# importing files:
	create_table.py -d TestDB.db file some.csv someOther.csv

### Generate renderable report ###

`construct_report.py` takes lots of files to generate a "renderable" (you guessed it) JSON file
containing all information that is needed to render a report:

	construct_report.py -r example_files/simplereport_model.json \
	                    -q example_files/eva_questions_pre_SS14.json \
	                    -a example_files/eva_answertypes.json \
	                    -d TestDB.db \
	                    -c HerrProfMustermannVKursXYZCSV
