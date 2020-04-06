import os
from os import path
from datetime import datetime
import pandas as pd


test_1_results_file = "1-OvenLoad.txt"


def read(folder):

    message_text = ""
    message_success = True
    result = ""
    time = ""
    table = {}
    i = 1

    full_path = folder + '\\' + test_1_results_file

    #print(full_path)

    if not path.os.path.isfile(full_path):
        message_text = message_text + " *** File not found!"
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
                table[i] = [line_splitted[0], str(int(line_splitted[0]) + 1), float(line_splitted[1]), float(line_splitted[2])]
                i = i + 1
                #print(line_splitted)

            if "DUT" in line and "VReg" in line and "ppm" in line and "_fPrint" not in line:
                start = True

        columns = ['DUT', 'pos', 'VReg', 'ppm']

        result = pd.DataFrame.from_dict(table, orient='index')
        result.columns = columns

        #print(result.info())

        message_success = True
        message_text = ""


    return message_success, message_text, test_1_results_file, time, result