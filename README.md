Adam
====

Adam is a tool usable for the teaching evaluation at the TU Dresden.
This version is completely rewritten using Python3 based on the most simple and basic requirements.
A basic GUI written for GTK3 is available.

Usage
-----

### Create tutor coding ###

#### JSON coding creation ####

`create_coding.py` can load multiple plain text files containing data about courses and their tutors and produce the corresponding JSON coding.
This JSON data can be printed to stdout:

    # Create coding from one or multiple plain text files
    create_coding.py course_abc.txt course_xyz.txt > file.json

Alternatively you can specify a file to save to save the coding to:

    create_coding.py course_abc.txt course_xyz.txt -o file.json

If you want to / can use the GUI, simply call `coding_gui.py`:

    coding_gui.py
    
#### Export into readable formats ####

`export_coding.py` takes the created JSON files and produces readable files from it:
either a simple plain text file

    export_coding.py plain -o outfile coding.json

or a fancy html table (that can be used for printing and showing in the lectures)

    export_coding.py html -o outfile.htm -s example_files/slides.css coding.json

### Import CSV into sqlite database ###

`create_table.py` *TODO: proper CLI*
