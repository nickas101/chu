import pandas as pd
from natsort import natsorted, ns

from . import file_opener
from . import frequency_reader


test_results_file = '4-Soft Vfy with comp numbers.txt'
accur = 4


def read(folder, limit):

    freq = ''
    bad_units = ''
    result_fvt = pd.DataFrame()
    result_calculated = pd.DataFrame()
    result_max = pd.DataFrame()
    result_min = pd.DataFrame()
    result_mean = pd.DataFrame()
    res_temp = pd.DataFrame()
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

            if 'DUT' in line and 'Temp' in line and 'ppm' in line and '_fPrint' not in line:
                start = True

            if '_define nominalFreq-' in line:
                freq = frequency_reader.read_frequency(line, '_define nominalFreq-')

        result_fvt = pd.DataFrame.from_dict(table, orient='index')
        result_fvt.columns = ['DUT', 'pos', 'Temp', 'ppm']

        result_fvt.sort_values(['pos', 'Temp'], ascending=[True, False], inplace=True)
        result_fvt.reset_index(inplace=True, drop=True)
        result_calculated['DUT'] =  result_fvt['DUT'].unique()
        result_calculated['pos'] = result_fvt['pos'].unique()

        result_fvt.loc[result_fvt['ppm'] < -10000, 'ppm'] = None
        result_fvt['ppm'] = result_fvt['ppm'].interpolate(limit = limit)

        result_fvt['mean_ppm'] = result_fvt.groupby('pos')['ppm'].transform('mean')
        result_fvt['ppb_norm'] = round(1000 * (result_fvt['ppm'] - result_fvt['mean_ppm']), accur)
        result_fvt['min_ppb_norm'] = result_fvt.groupby('pos')['ppb_norm'].transform('min')
        result_fvt['max_ppb_norm'] = result_fvt.groupby('pos')['ppb_norm'].transform('max')

        result_calculated = result_fvt.groupby(['DUT', 'pos', 'mean_ppm', 'min_ppb_norm', 'max_ppb_norm']).count().reset_index()
        result_calculated.drop(['Temp', 'ppm', 'ppb_norm'], axis='columns', inplace=True)
        result_calculated.sort_values(['pos'], ascending=[True], inplace=True)
        result_calculated = result_calculated.reset_index(drop=True)
        result_calculated['mean_ppm'] = round(result_calculated['mean_ppm'], accur)

        result_fvt.sort_values(['pos', 'Temp'], ascending=[True, False], inplace=True)
        bad_units_df = result_fvt.copy()

        bad_units_ppm = bad_units_df[bad_units_df['ppm'].isna()]
        bad_units_list = natsorted(bad_units_ppm['DUT'].unique().tolist())
        bad_units = bad_units + " " + ", ".join(str(int(x)) for x in bad_units_list)

        # result_cutted = result_fvt[~result_fvt['DUT'].isin(bad_units_list)]

    else:
        message_text = message_text + '(' + test_results_file + ')  '

    return message_success, message_text, test_results_file, freq, time, bad_units, result_fvt, result_calculated
