import pandas as pd
from natsort import natsorted, ns


def convert(input_table):

    output_table = pd.DataFrame()

    output_table['DUT'] = input_table['DUT'].astype(int)
    output_table['DUT'] = output_table['DUT'].astype(str)
    output_table['pos'] = input_table['pos'].astype(int)

    for column in input_table.columns:
        if column != 'DUT' and column != 'pos':
            column_name = 'Table-' + str(column)
            output_table[column_name] = input_table[column]
            output_table[column_name] = output_table[output_table[column_name].notna()][column_name].astype(int)

    bad_units = find_bad_units(output_table)

    return output_table, bad_units


def convert_short(input_table):

    output_table = pd.DataFrame()

    output_table['DUT'] = input_table['DUT'].astype(int)
    output_table['DUT'] = output_table['DUT'].astype(str)
    output_table['pos'] = input_table['pos'].astype(int)

    for column in input_table.columns:
        if column != 'DUT' and column != 'pos':
            column_name = str(column)
            output_table[column_name] = input_table[column]
            output_table[column_name] = output_table[output_table[column_name].notna()][column_name].astype(int)

    bad_units = find_bad_units(output_table)

    return output_table, bad_units


def find_bad_units(table):
    bad_units = ''
    # print(table)

    # bad_units_df = table[table.isna().any(axis='columns')]['pos']
    # # bad_units_df.sort_values(['pos'], ascending=[True], inplace=True)
    # print(bad_units_df)
    #
    # bad_units_list = natsorted(bad_units_df['pos'].unique().tolist())
    # bad_units = bad_units + " " + ", ".join(str(int(x)) for x in bad_units_list)

    return bad_units
