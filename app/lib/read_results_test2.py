import pandas as pd

from . import file_opener
from . import frequency_reader


test_results_file = '2 -SetUpVreg.txt'


def read(folder):

    result = pd.DataFrame()
    freq = ''
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
                table[index] = [line_splitted[0], int(line_splitted[0]) + 1, float(line_splitted[1]), int(line_splitted[2]), int(line_splitted[3]), float(line_splitted[4])]
                index = index + 1

            if 'DUT' in line and 'Temp' in line and 'VReg_Trim' in line and 'TcVReg_Trim' in line and '_fPrint' not in line:
                start = True

            if '_define nominalFreq-' in line:
                freq = frequency_reader.read_frequency(line, '_define nominalFreq-')

        result = pd.DataFrame.from_dict(table, orient='index')
        result.columns = ['DUT', 'pos', 'Temp', 'VReg_Trim', 'TcVReg_Trim', 'V']

        # temporary create column 'temp_rounded' to sort by temperature
        result['temp_rounded'] = round(result['Temp'], 0)
        result.sort_values(['pos', 'temp_rounded', 'VReg_Trim', 'TcVReg_Trim'], ascending=[True, True, True, True], inplace=True)
        result.drop('temp_rounded', 1, inplace=True)


    return message_success, message_text, test_results_file, freq, time, result