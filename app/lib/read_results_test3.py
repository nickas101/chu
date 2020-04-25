import pandas as pd
from natsort import natsorted, ns

from . import file_opener
from . import frequency_reader


test_results_file = '3-Comp.txt'


def read(folder, limit):

    freq = ''
    bad_units = ''
    result_full = pd.DataFrame()
    result_cutted = pd.DataFrame()
    vreg_table_from_test3 = pd.DataFrame()
    res_temp = pd.DataFrame()
    table = {}
    card_0 = []
    card_1 = []
    table_0 = []
    table_1 = []
    index = 1

    message_success, message_text, time, lines = file_opener.open_file(folder, test_results_file)

    if message_success:

        start = False
        stop = False
        dut_temp = ''
        temperature_temp = ''
        residual_temp = ''
        for line in lines:
            if 'Script completed' in line or 'Above measuremnts' in line:
                stop = True

            if start and not stop and line != '' and line != "\n":
                line_splitted = line.split("\t")
                if len(line_splitted) < 5:
                    dut_temp = line_splitted[0]
                    temperature_temp = float(line_splitted[1])
                    residual_temp = line_splitted[2]
                elif line_splitted[0] == dut_temp and round(float(line_splitted[1]), 0) == round(temperature_temp, 0):
                    table[index] = [line_splitted[0], int(line_splitted[0]) + 1, float(residual_temp), int(round(float(line_splitted[1]),0)), int(line_splitted[2]), int(line_splitted[3]), float(line_splitted[4])]
                    index = index + 1
                else:
                    table[index] = [line_splitted[0], int(line_splitted[0]) + 1, None,
                                float(line_splitted[1]), int(line_splitted[2]), int(line_splitted[3]),
                                float(line_splitted[4])]
                    index = index + 1

            if 'DUT' in line and 'Temp' in line and 'CoeffB' in line and 'CoeffC' in line and 'ppm' in line and '_fPrint' not in line:
                start = True

            if '_define nominalFreq-' in line:
                freq = frequency_reader.read_frequency(line, '_define nominalFreq-')

            if '_define TableForCrd-0 [' in line:
                card_0 = line_to_list(line, '_define TableForCrd-0 ')

            if '_define TableForCrd-1 [' in line:
                card_1 = line_to_list(line, '_define TableForCrd-1 ')

            if '_define Table-0 [' in line:
                table_0 = line_to_list(line, '_define Table-0 ')

            if '_define Table-1 [' in line:
                table_1 = line_to_list(line, '_define Table-1 ')


        poses = list(map(int, card_0 + card_1))

        vreg_table_from_test3['pos'] = poses
        vreg_table_from_test3['Table-0'] = list(map(int, table_0))
        vreg_table_from_test3['Table-1'] = list(map(int, table_1))
        vreg_table_from_test3['DUT'] = (vreg_table_from_test3['pos'] - 1).astype(str)
        vreg_table_from_test3 = vreg_table_from_test3[['DUT', 'pos', 'Table-0', 'Table-1']]


        result_full = pd.DataFrame.from_dict(table, orient='index')
        result_full.columns = ['DUT', 'pos', 'residual', 'Temp', 'CoeffB', 'CoeffC', 'ppm']

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

        poses_result = result_full['pos'].unique().tolist()

        for pos_result in poses_result:
            result_full_single = result_full[result_full['pos'] == pos_result]
            residual_average = result_full_single['residual'].mean()
            #result_full_single['residual_norm_ppb'] = 1000 * (result_full_single['residual'] - residual_average)
            result_full_single['residual_norm_ppb'] = 1000 * (
                        result_full.loc[result_full['pos'] == pos_result, ['residual']] - residual_average)
            res_temp = pd.concat([res_temp, result_full_single])

        #print(res_temp)

        res_temp = res_temp[['DUT', 'pos', 'residual', 'residual_norm_ppb', 'Temp', 'CoeffB', 'CoeffC', 'ppm']]

        result_cutted = res_temp[~res_temp['pos'].isin(bad_units_list)]

        # to serilise a dataframe
        # result_full.to_pickle('app/scripts/read_test_3.pkl')
        # unpickled_df = pd.read_pickle('app/scripts/read_test_3.pkl')
        # print(unpickled_df)

    else:
        message_text = message_text + '(' + test_results_file + ')  '


    return message_success, message_text, test_results_file, freq, time, bad_units, res_temp, result_cutted, vreg_table_from_test3


def line_to_list(line, input_string):

    line = line.replace("\n", '')
    line = line.replace(';', '')
    line_splitted = line.split("\t")
    line_2 = line_splitted[1].replace(input_string, '')
    output_list = line_2.split(' ')
    output_list.pop(0)

    return output_list