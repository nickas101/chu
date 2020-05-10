"""Calculate VReg for a test-3 preparation

The module is to substitute '2- SetUpVreg Calculator.xlsx' file

Parameters
----------
df : Pandas DataFrame
    From test-2 results
    DataFrame with columns = ['DUT'(object), 'pos'(int64),
                            'Temp'(float64), 'VReg_Trim'(int64),
                            'TcVReg_Trim'(int64), 'V'(float64)]

Returns
-------
result_df: Pandas DataFrame
    Output DataFrame with columns = ['DUT'(object), 'pos'(int64), 'Table-0'(int64), 'Table-1'(int64)]
"""

import pandas as pd
import numpy as np


def calculate(df):
    """Calculate VReg for a test-3 preparation"""

    t1 = 25
    output_dict = {}
    index = 0

    input_df = df.copy()

    duts = input_df['DUT'].unique().tolist()
    input_df['V2'] = input_df['V'] - 2

    for dut in duts:
        df_dt = input_df[input_df['DUT'] == dut]
        vregs = df_dt['VReg_Trim'].unique().tolist()

        temp_low = df_dt[df_dt['Temp'] < (t1 + 3)]['Temp'].tolist()[0]
        temp_high = df_dt[df_dt['Temp'] > (t1 + 4)]['Temp'].tolist()[0]

        temp = {}
        norm_V = {}
        tc_vreg_zero_slope = {}
        second_order_curve_fit = {}

        for vreg in vregs:
            df_dt_vreg = df_dt[df_dt['VReg_Trim'] == vreg]
            tc_vregs = df_dt_vreg['TcVReg_Trim'].unique().tolist()

            slope = {}
            shift = {}

            for tc_vreg in tc_vregs:
                df_dt_tc_vreg = df_dt_vreg[df_dt_vreg['TcVReg_Trim'] == tc_vreg]

                v2_t1 = df_dt_tc_vreg[df_dt_tc_vreg['Temp'] < (t1 + 3)]['V2'].tolist()[0]
                v2_t2 = df_dt_tc_vreg[df_dt_tc_vreg['Temp'] > (t1 + 4)]['V2'].tolist()[0]

                slope[tc_vreg] = (v2_t2 - v2_t1) / (temp_high - temp_low)
                shift[tc_vreg] = v2_t1 - (slope[tc_vreg] * temp_low)

            temp[vreg] = (list(shift.values())[-1] - list(shift.values())[0]) / (list(slope.values())[0] - list(slope.values())[-1])
            norm_V[vreg] = list(slope.values())[0] * temp[vreg] + list(shift.values())[0]
            tc_vreg_zero_slope[vreg] = 5 - 25 * list(slope.values())[0] / (list(slope.values())[-1] - list(slope.values())[0])


        Vreg_Trim = round(-list(norm_V.values())[0] * 10 / (list(norm_V.values())[-1] - list(norm_V.values())[0]), 0)

        coefficients = np.polyfit(vregs, list(tc_vreg_zero_slope.values()), 2)

        for vreg in vregs:
            second_order_curve_fit[vreg] = coefficients[0] * vreg * vreg + coefficients[1] * vreg + coefficients[2]

        TcVreg_Trim = round(coefficients[0] * Vreg_Trim * Vreg_Trim + coefficients[1] * Vreg_Trim + coefficients[2],0)

        output_dict[index] = [dut, df_dt['pos'].tolist()[0], int(Vreg_Trim), int(TcVreg_Trim)]
        index = index + 1

    columns = ['DUT', 'pos', 'Table-0', 'Table-1']
    result_df = pd.DataFrame.from_dict(output_dict, orient='index')
    result_df.columns = columns

    return result_df
