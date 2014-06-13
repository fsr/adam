# !/usr/bin/python3
import json
import argparse

import create_coding

# Creates a JSON file defining the questions from a plain text file
# and validates them with a given answer type JSON file.

def parse_question_data_from_file(f):
    questions = []
    for line in f:
        # Remove newline at the end
        line = line[:-1]
        # Filter comments
        if line.startswith("#") or not line:
            continue

        # Regular question line: name, type, text
        (qname, qtype, qtext) = tuple(map(lambda s: s.strip(), line.split(",", 2)))

        # metaquestions
        if qtype == "?":
            questions.append({"name": qname, "type": qtype, "text": qtext, "answers": []})
        # subquestions
        elif qtype.startswith("!"):
            # I don't know how to Python.
            def q_with_new_answer(q, ans):
                q["answers"].append(ans);
                return q;

            questions = list(map(lambda q: q_with_new_answer(q, qtext) if q["name"] == qtype[1:] else q, questions))
        # regular questions
        else:
            questions.append({"name": qname, "type": qtype, "text": qtext})
    return questions


def is_question_json_valid(questions, definitions):
    # Standard types
    valid_types = ["?", "tc16", "tc8", "tc4", "tc2", "tc1"]
    for qdef in definitions:
        valid_types.append(qdef["type"])
    # Metaquestion-Types
    for question in questions:
        if question["type"] == "?":
            valid_types.append("!" + question["name"])

    for question in questions:
        qtype = question["type"]

        if qtype.endswith("+"):
            qtype = qtype[:-1]

        if qtype in valid_types:
            pass
        else:
            return False
    return True


if __name__ == '__main__':
    # CLI argument parsing
    parser = argparse.ArgumentParser(
        description="Create JSON coding for questions from plain text files.")
    parser.add_argument('inputfile', type=argparse.FileType('r'), nargs=1, help="plain text question file")
    parser.add_argument("-d", "--definitions", nargs=1,
                        help="question type definitions the plain text file can be checked against")
    parser.add_argument("-o", "--output", nargs=1, help="JSON file the output is to be stored in")

    args = parser.parse_args()

    questions = parse_question_data_from_file(args.inputfile[0])
    json_coding = create_coding.prettyprint_json(questions)

    if args.definitions:
        with open(args.definitions[0], 'r') as f:
            if not is_question_json_valid(questions, json.load(f)):
                raise Exception("The JSON file created is not compatible with the supplied definition file!")

    if not args.output:
        print(json_coding)
    else:
        with open(args.output[0], 'w') as f:
            f.write(json_coding)
