import os
from os import path
from datetime import datetime
import pandas as pd
from pathlib import Path


test_results_file = "2 -SetUpVreg.txt"


def read(folder):

    message_text = ""
    message_success = True
    result = pd.DataFrame()
    time = ""
    freq = ""
    table = {}
    index = 1

    data_folder = Path(folder)
    full_path = data_folder / test_results_file

    if not path.os.path.isfile(full_path):
        message_text = message_text + " *** Input file not found!"
        message_success = False
    else:
        time_raw = os.path.getmtime(full_path)
        time_string = str(datetime.fromtimestamp(time_raw))
        time = time_string.split('.')[0]

        with open(full_path, 'r') as file:
            lines = file.readlines()

        start = False
        stop = False
        for line in lines:
            if "Script completed" in line or "Above measuremnts" in line:
                stop = True

            if start and not stop and line != "" and line != "\n":
                line_splitted = line.split("\t")
                table[index] = [line_splitted[0], int(line_splitted[0]) + 1, float(line_splitted[1]), int(line_splitted[2]), int(line_splitted[3]), float(line_splitted[4])]
                index = index + 1

            if "DUT" in line and "Temp" in line and "VReg_Trim" in line and "TcVReg_Trim" in line and "_fPrint" not in line:
                start = True

            if "_define nominalFreq-" in line:
                freq_splitted = line.split("\t")
                freq = freq_splitted[1].replace("_define nominalFreq-", "")
                freq = freq.replace(";", "")


        columns = ['DUT', 'pos', 'Temp', 'VReg_Trim', 'TcVReg_Trim', 'V']

        result = pd.DataFrame.from_dict(table, orient='index')
        result.columns = columns


        result['temp_rounded'] = round(result['Temp'], 0)
        result.sort_values(['pos', 'temp_rounded', 'VReg_Trim', 'TcVReg_Trim'], ascending=[True, True, True, True], inplace=True)
        result.drop('temp_rounded', 1, inplace=True)


    return message_success, message_text, test_results_file, freq, time, result