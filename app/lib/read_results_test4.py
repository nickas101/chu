import os
from os import path
from datetime import datetime
import pandas as pd
from pathlib import Path
from natsort import natsorted, ns


test_results_file = "4-Soft Vfy with comp numbers.txt"


def read(folder, limit):

    message_text = ""
    message_success = True
    time = ""
    freq = ""
    bad_units = ""
    result_fvt = pd.DataFrame()
    result_calculated = pd.DataFrame()
    table = {}
    i = 1

    data_folder = Path(folder)
    full_path = data_folder / test_results_file
    print(full_path)

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
                print(line_splitted)
                table[i] = [line_splitted[0], int(line_splitted[0]) + 1, float(line_splitted[1]), float(line_splitted[2])]
                i = i + 1


            if "DUT" in line and "Temp" in line and "ppm" in line and "_fPrint" not in line:
                start = True

            if "_define nominalFreq-" in line:
                freq_splitted = line.split("\t")
                freq = freq_splitted[1].replace("_define nominalFreq-", "")
                freq = freq.replace(";", "")
                #freq = float(freq)


        columns = ['DUT', 'pos', 'Temp', 'ppm']

        result_fvt = pd.DataFrame.from_dict(table, orient='index')
        result_fvt.columns = columns

        result_fvt.sort_values(['pos', 'Temp'], ascending=[True, False], inplace=True)
        result_fvt.reset_index(inplace=True, drop=True)

        # print(result_fvt)

        result_fvt.loc[result_fvt['ppm'] < -10000, 'ppm'] = None

        result_fvt['ppm'] = result_fvt['ppm'].interpolate(limit = limit)

        bad_units_df = result_fvt.copy()

        bad_units_ppm = bad_units_df[bad_units_df['ppm'].isna()]

        bad_units_ppm.sort_values(['DUT'], ascending=[True], inplace=True)

        bad_units_list = natsorted(bad_units_ppm['DUT'].unique().tolist())

        bad_units = bad_units + " " + ", ".join(str(int(x)) for x in bad_units_list)

        result_cutted = result_fvt[~result_fvt['DUT'].isin(bad_units_list)]
        #rslt_df = dataframe.loc[~dataframe['Stream'].isin(options)]

        # print(bad_units)
        # print(result_full)
        # print(result_cutted)
        # print(result_full.info())

        result_fvt.to_pickle("app/scripts/read_test_3.pkl")
        #unpickled_df = pd.read_pickle("app/scripts/read_test_3.pkl")
        #print(unpickled_df)

        message_success = True
        message_text = ""


    return message_success, message_text, test_results_file, freq, time, bad_units, result_fvt, result_calculated