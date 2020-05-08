import pandas as pd


def convert(input_table):

    output_table = pd.DataFrame()

    output_table['DUT'] = input_table['DUT'].astype(int)
    output_table['DUT'] = output_table['DUT'].astype(str)
    output_table['pos'] = input_table['pos'].astype(int)

    for column in input_table.columns:
        if column != 'DUT' and column != 'pos':
            column_name = 'Table-' + str(column)
            output_table[column_name] = input_table[column].astype(int)

    return output_table


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

    return output_table
