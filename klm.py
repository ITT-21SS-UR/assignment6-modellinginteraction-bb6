
"""
Pass setup.json file on start up
File should look like this
{
    "k": 0.28,
    "p": 1.1,
    "h": 0.4,
    "b": 0.1,
    "m": 1.35,
    "operator_file": "klm.txt"
}
all single characters are the time values for operators, can be changed as needed, as long as they match the operators
used in the operator_file
operator_file should be a text file containing the all operators used for the task (i.e: k2bp2bh8k). Operators can be
split up in multiple lines and can contain comments prefixed with a #

Script by Kay Brinkmann
"""


import sys
import json


# turn file with task operators into string without whitespaces
def file_to_klm_string(filename):
    klm_string = ""
    try:
        file = open(filename)
    except IOError:
        return []
    lines = file.readlines()
    for line in lines:
        new_line = line.split("#", 1)[0].replace(" ", "").rstrip().lower()
        klm_string += new_line
    return klm_string


# calculates task time
def calculate_klm_time(klm_model, klm_string):
    numbers = ""
    result = 0
    for char in klm_string:
        # save digits as prefixes for following operator
        if char.isdigit():
            numbers += char
        else:
            try:
                operator_number = klm_model[char]
            except KeyError:
                print(char, ' character does not match any klm operator. Check your klm file.')
                return
            # multiply by prefixed number if it exists
            if len(numbers) > 0:
                operator_number *= float(numbers)
                numbers = ""
            result += operator_number
    return result


# parses json file to dict
def parse_config(file):
    try:
        with open(str(file)) as f:
            setup_dict = json.load(f)
    except Exception as e:
        print(e, ": could not read setup file!")
        sys.exit()
    return setup_dict


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("you need to pass a setup file!")
        sys.exit()
    klm_dict = parse_config(sys.argv[1])
    try:
        klm_string = file_to_klm_string(klm_dict["operator_file"])
    except Exception as e:
        print(e, ": could not read operator file!")
        sys.exit()
    print("klm string: ", klm_string)
    print("Expected task completion time = ", calculate_klm_time(klm_dict, klm_string))


if __name__ == '__main__':
    main()
