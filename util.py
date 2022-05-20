import defs

from os.path import isfile


# Used to get a valid string from the user
def get_valid_string(str_input):

    while True:
        try:
            ans = input(str_input + '\n')

            if len(ans) > 0:
                break
        except ValueError:
            print(defs.INPUT_INVALID)

    return ans


# Used to get a valid integer from the user
def get_valid_int(str_input, min_num, max_num):

    while True:
        try:
            ans = int(input(str_input + '\n'))

            if min_num <= ans <= max_num:
                break

        except ValueError:
            print(defs.INPUT_INVALID)

    return ans

