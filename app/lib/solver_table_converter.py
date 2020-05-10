"""Converts table from a solver to the right format

Parameters
----------
input_table : Pandas DataFrame
    DataFrame from solver

Returns
-------
output_table_short: Pandas DataFrame
    converted table with column names as table numbers
output_table: Pandas DataFrame
    converted table with column names as a string
bad_units: str
    string line of bad units positions
bad_units_list: list
    a list of bad units
"""

import pandas as pd
from natsort import natsorted


def convert(input_table):
    """Converts solver output into the right format."""

    output_table = pd.DataFrame()

    output_table['DUT'] = input_table['DUT'].astype(int)
    output_table['DUT'] = output_table['DUT'].astype(str)
    output_table['pos'] = input_table['pos'].astype(int)

    output_table_short = output_table.copy()

    for column in input_table.columns:
        if column != 'DUT' and column != 'pos':
            column_name = 'Table-' + str(column)
            column_name_short = str(column)
            output_table[column_name] = input_table[column].astype(pd.Int64Dtype())
            output_table_short[column_name_short] = input_table[column].astype(pd.Int64Dtype())

    bad_units_df = output_table[output_table.isna().any(axis='columns')]

    bad_units_list = natsorted(bad_units_df['pos'].unique().tolist())
    bad_units = ', '.join(str(int(x)) for x in bad_units_list)

    return output_table_short, output_table, bad_units, bad_units_list
