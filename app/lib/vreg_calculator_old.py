# The module is to substitute '2- SetUpVreg Calculator.xlsx' file
# to calculate VReg for a test-3 preparation
#
# Input: Pandas DataFrame with columns = ['DUT'(object), 'pos'(int64), 'Temp'(float64), 'VReg_Trim'(int64), 'TcVReg_Trim'(int64), 'V'(float64)]
# Output: Pandas DataFrame with columns = ['DUT'(object), 'pos'(int64), 'Table-0'(int64), 'Table-1'(int64)]

import pandas as pd
import numpy as np




def calculate(input_df):

    t1 = 25
    output_dict = {}
    i = 0

    duts = input_df['DUT'].unique().tolist()

    for dut in duts:

        df_dt = input_df[input_df['DUT'] == dut]

        df_dt_t1 = df_dt[df_dt['Temp'] < (t1 + 3)]
        df_dt_t2 = df_dt[df_dt['Temp'] > (t1 + 4)]

        df_dt_t1_0 = df_dt_t1[df_dt_t1['VReg_Trim'] == 0]
        df_dt_t1_5 = df_dt_t1[df_dt_t1['VReg_Trim'] == 5]
        df_dt_t1_10 = df_dt_t1[df_dt_t1['VReg_Trim'] == 10]
        df_dt_t2_0 = df_dt_t2[df_dt_t2['VReg_Trim'] == 0]
        df_dt_t2_5 = df_dt_t2[df_dt_t2['VReg_Trim'] == 5]
        df_dt_t2_10 = df_dt_t2[df_dt_t2['VReg_Trim'] == 10]

        df_dt_t1_0_5 = df_dt_t1_0[df_dt_t1_0['TcVReg_Trim'] == 5]
        df_dt_t1_0_30 = df_dt_t1_0[df_dt_t1_0['TcVReg_Trim'] == 30]
        df_dt_t1_5_5 = df_dt_t1_5[df_dt_t1_5['TcVReg_Trim'] == 5]
        df_dt_t1_5_30 = df_dt_t1_5[df_dt_t1_5['TcVReg_Trim'] == 30]
        df_dt_t1_10_5 = df_dt_t1_10[df_dt_t1_10['TcVReg_Trim'] == 5]
        df_dt_t1_10_30 = df_dt_t1_10[df_dt_t1_10['TcVReg_Trim'] == 30]

        df_dt_t2_0_5 = df_dt_t2_0[df_dt_t2_0['TcVReg_Trim'] == 5]
        df_dt_t2_0_30 = df_dt_t2_0[df_dt_t2_0['TcVReg_Trim'] == 30]
        df_dt_t2_5_5 = df_dt_t2_5[df_dt_t2_5['TcVReg_Trim'] == 5]
        df_dt_t2_5_30 = df_dt_t2_5[df_dt_t2_5['TcVReg_Trim'] == 30]
        df_dt_t2_10_5 = df_dt_t2_10[df_dt_t2_10['TcVReg_Trim'] == 5]
        df_dt_t2_10_30 = df_dt_t2_10[df_dt_t2_10['TcVReg_Trim'] == 30]


        C7 = df_dt_t1_0_5['Temp'].tolist()[0]
        C13 = df_dt_t2_0_5['Temp'].tolist()[0]
        F7 = df_dt_t1_0_5['V'].tolist()[0]
        F13 = df_dt_t2_0_5['V'].tolist()[0]
        F8 = df_dt_t1_0_30['V'].tolist()[0]
        F9 = df_dt_t1_5_5['V'].tolist()[0]
        F14 = df_dt_t2_0_30['V'].tolist()[0]
        F15 = df_dt_t2_5_5['V'].tolist()[0]
        F16 = df_dt_t2_5_30['V'].tolist()[0]
        F10 = df_dt_t1_5_30['V'].tolist()[0]
        F11 = df_dt_t1_10_5['V'].tolist()[0]
        F17 = df_dt_t2_10_5['V'].tolist()[0]
        F12 = df_dt_t1_10_30['V'].tolist()[0]
        F18 = df_dt_t2_10_30['V'].tolist()[0]

        Vreg_Trims_t1 = df_dt_t1['VReg_Trim'].unique().tolist()

        D7 = Vreg_Trims_t1[0]
        D9 = Vreg_Trims_t1[1]
        D11 = Vreg_Trims_t1[-1]

        C22 = C7
        C23 = C13
        D22 = F7-2
        D23 = F13-2
        E22 = F8-2
        E23 = F14-2
        F22 = F9-2
        F23 = F15-2
        G22 = F10-2
        G23 = F16-2
        H22 = F11-2
        H23 = F17-2
        I22 = F12-2
        I23 = F18-2

        # print('C22 = ' + str(C22))
        # print('C23 = ' + str(C23))
        # print('D22 = ' + str(D22))
        # print('D23 = ' + str(D23))
        # print('E22 = ' + str(E22))
        # print('E23 = ' + str(E23))
        # print('F22 = ' + str(F22))
        # print('F23 = ' + str(F23))
        # print('G22 = ' + str(G22))
        # print('G23 = ' + str(G23))
        # print('H22 = ' + str(H22))
        # print('H23 = ' + str(H23))
        # print('I22 = ' + str(I22))
        # print('I23 = ' + str(I23))


        E24 = (E23-E22)/(C23-C22)
        E25 = E22-E24*D22

        I24 = (I23-I22)/(C23-C22)
        I25 = I22-I24*H22

        H24 = (H23-H22)/(C23-C22)
        H25 = H22-H24*G22


        F24 = (F23-F22)/(C23-C22)
        G24 = (G23-G22)/(C23-C22)

        # 0:5
        D24 = (D23 - D22) / (C23 - C22)
        D25 = D22-D24*C22

        G35 = (E25-D25)/(D24-E24)
        G37 = (I25-H25)/(H24-I24)

        H35 = D24*G35+D25
        H37 = H24*G37+H25

        G48 = 5-D24*25/(E24-D24)
        G49 = 5-F24*25/(G24-F24)
        G50 = 5-H24*25/(I24-H24)

        F48 = D7
        F49 = D9
        F50 = D11

        ys = [G48, G49, G50]
        xs = [F48, F49, F50]

        coefficients = np.polyfit(xs, ys, 2)

        #print(coefficients)

        J48 = coefficients[2]
        J49 = coefficients[1]
        J50 = coefficients[0]

        H38 = -H35 * 10 / (H37 - H35)
        H51 = J50*H38*H38+J49*H38+J48

        Vreg_Trim = round(H38, 0)
        TcVreg_Trim = round(H51,0)

        # print("Vreg_Trim = " + str(Vreg_Trim))
        # print("TcVreg_Trim = " + str(TcVreg_Trim))

        output_dict[i] = [dut, df_dt['pos'].tolist()[0], int(Vreg_Trim), int(TcVreg_Trim)]
        i = i + 1


    columns = ['DUT', 'pos', 'Table-0', 'Table-1']
    result_df = pd.DataFrame.from_dict(output_dict, orient='index')
    result_df.columns = columns

    #print(result_df)

    return result_df