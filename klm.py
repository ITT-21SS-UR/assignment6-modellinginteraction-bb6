# This Python file uses the following encoding: utf-8
import sys
import json


def file_to_klm_string(filename):
    klm_string = ""
    try:
        file = open(filename)
    except IOError:
        return []
    lines = file.readlines()
    for line in lines:
        split = line.split("#", 1)
        new_line = split[0]
        klm_string += new_line

    return klm_string.replace(" ", "").lower()


def calculate_klm_time(klm_model, klm_string):
    numbers = ""
    result = 0
    for char in klm_string:
        if char.isdigit():
            numbers += char
        else:
            try:
                operator_number = klm_model[char]
            except KeyError:
                print(char, ' character does not match any klm operator. Check your klm file.')
                return

            if len(numbers) > 0:
                operator_number *= float(numbers)
                numbers = ""
            result += operator_number
    return result


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
    print("klm string: ", file_to_klm_string("klm.txt"))
    print("Expected task completion time = ", calculate_klm_time(klm_dict, klm_string))


if __name__ == '__main__':
    main()
