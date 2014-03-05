Adam
====

Adam is a tool usable for the teaching evaluation at the TU Dresden.
This version is completely rewritten using Python3 based on the most simple and basic requirements.
A basic GUI written in GTK3 is available.

Usage
-----

create_coding.py can load multiple plain text files and produce the corresponding JSON coding.
This JSON data can be printed to stdout and redirected into a file by the user using the shell:

    # Create coding from one or multiple plain text files and save to file.json
    create_coding.py course_abc.txt course_xyz.txt > file.json

Alternatively you can specify a file to save to save the configuration to:

    create_coding.py course_abc.txt course_xyz.txt -o file.json

If you want to / can use the GUI, call:

    coding_gui.py
