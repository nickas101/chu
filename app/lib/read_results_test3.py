import os
from os import path
from datetime import datetime
import pandas as pd
from pathlib import Path
from natsort import natsorted, ns


test_results_file = "3-Comp.txt"


def read(folder, limit):

    message_text = ""
    message_success = True
    time = ""
    freq = ""
    bad_units = ""
    result_full = pd.DataFrame()
    result_cutted = pd.DataFrame()
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
        dut_temp = ""
        temperature_temp = ""
        residual_temp = ""
        for line in lines:
            if "Script completed" in line or "Above measuremnts" in line:
                stop = True

            if start and not stop and line != "" and line != "\n":
                line_splitted = line.split("\t")
                if len(line_splitted) < 5:
                    dut_temp = line_splitted[0]
                    temperature_temp = float(line_splitted[1])
                    residual_temp = line_splitted[2]
                elif line_splitted[0] == dut_temp and round(float(line_splitted[1]), 0) == round(temperature_temp, 0):
                    table[i] = [line_splitted[0], int(line_splitted[0]) + 1, float(residual_temp), int(round(float(line_splitted[1]),0)), int(line_splitted[2]), int(line_splitted[3]), float(line_splitted[4])]
                    i = i + 1
                else:
                    table[i] = [line_splitted[0], int(line_splitted[0]) + 1, None,
                                float(line_splitted[1]), int(line_splitted[2]), int(line_splitted[3]),
                                float(line_splitted[4])]
                    i = i + 1


            if "DUT" in line and "Temp" in line and "CoeffB" in line and "CoeffC" in line and "ppm" in line and "_fPrint" not in line:
                start = True

            if "_define nominalFreq-" in line:
                freq_splitted = line.split("\t")
                freq = freq_splitted[1].replace("_define nominalFreq-", "")
                freq = freq.replace(";", "")
                #freq = float(freq)


        columns = ['DUT', 'pos', 'residual', 'Temp', 'CoeffB', 'CoeffC', 'ppm']

        result_full = pd.DataFrame.from_dict(table, orient='index')
        result_full.columns = columns

        result_full.sort_values(['pos', 'Temp'], ascending=[True, False], inplace=True)
        result_full.reset_index(inplace=True, drop=True)

        result_full.loc[result_full['residual'] < -10000, 'residual'] = None
        result_full.loc[result_full['ppm'] < -10000, 'ppm'] = None

        result_full['ppm'] = result_full['ppm'].interpolate(limit = limit)
        result_full['residual'] = result_full['residual'].interpolate(limit = limit)

        bad_units_df = result_full.copy()

        bad_units_residual = bad_units_df[bad_units_df['residual'].isna()]
        bad_units_ppm = bad_units_df[bad_units_df['ppm'].isna()]

        bad_units_append = bad_units_residual.append(bad_units_ppm)

        bad_units_append.sort_values(['pos'], ascending=[True], inplace=True)

        bad_units_list = natsorted(bad_units_append['pos'].unique().tolist())

        bad_units = bad_units + " " + ", ".join(str(int(x)) for x in bad_units_list)

        result_cutted = result_full[~result_full['pos'].isin(bad_units_list)]
        #rslt_df = dataframe.loc[~dataframe['Stream'].isin(options)]

        # print(bad_units)
        # print(result_full)
        # print(result_cutted)
        # print(result_full.info())

        result_full.to_pickle("app/scripts/read_test_3.pkl")
        #unpickled_df = pd.read_pickle("app/scripts/read_test_3.pkl")
        #print(unpickled_df)

        message_success = True
        message_text = ""


    return message_success, message_text, test_results_file, freq, time, bad_units, result_full, result_cutted