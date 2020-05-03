import pandas as pd

from . import file_opener


test_results_file = '1-OvenLoad.txt'


def read(folder):

    result = pd.DataFrame()
    table = {}
    index = 1

    message_success, message_text, time, lines = file_opener.open_file(folder, test_results_file)

    if message_success:

        start = False
        stop = False
        for line in lines:
            if 'Script completed' in line or 'Above measuremnts' in line:
                stop = True

            if start and not stop and line != '' and line != "\n":
                line_splitted = line.split("\t")
                table[index] = [line_splitted[0], int(line_splitted[0]) + 1, float(line_splitted[1]), float(line_splitted[2])]
                index = index + 1

            if 'DUT' in line and 'VReg' in line and 'ppm' in line and '_fPrint' not in line:
                start = True

        result = pd.DataFrame.from_dict(table, orient='index')
        result.columns = ['DUT', 'pos', 'VReg', 'ppm']

    return message_success, message_text, test_results_file, time, result
