# This Python file uses the following encoding: utf-8


klm_own_model = {}
klm_standard_model = {
    "k": 0.28,
    "p": 1.1,
    "h": 0.4,
    "b": 0.1,
    "m": 1.35
}


def file_to_klm_string(filename):
    klm_string = ""
    try:
        file = open(filename)
    except IOError:
        return []
    lines = file.readlines()
    for line in lines:
        split = line.split("#",1)
        print("line : ", split)
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
            print("+", operator_number)
            result += operator_number
    return result


klm_string = file_to_klm_string("klm.txt")
print("klm string: ", file_to_klm_string("klm.txt"))
print("result with standard klm values: ", calculate_klm_time(klm_standard_model, klm_string))